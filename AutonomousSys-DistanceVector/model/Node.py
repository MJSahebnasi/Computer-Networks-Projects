import json
import socket
import threading
import time
from model.data_sharing_protocol import TableContainer, EdgeContainer


class Node:
    """
    After init, neighbors and routing_table are not set.
    Just use add_update_neighbor(). The routing_table will automatically be updated.
    """

    def __init__(self, id, listening_port, host):
        """
        :param id: int
        :param listening_port: int
        :param host: str
        """
        self.id = id
        self.listening_port = listening_port
        self.host = host
        self.last_time_table_sent = time.time()
        self.update_period = 30  # seconds
        self.has_sent_table_for_once = False
        self.stop_event = threading.Event() # for both perio and server

        self.neighbors = {}
        # contains (node_id: (host, port)) items

        self.routing_table = {self.id: (None, 0)}
        # contains {node_id: (next_node_id, path_cost)} key-value pairs
        # next_node_id determines the next node to see when routing to the node (with node_id)

        # constantly listening:
        t = threading.Thread(target=self.listening_server, args=(self.stop_event,))
        t.setDaemon(True)
        t.start()

        # periodically updating:
        t = threading.Thread(target=self.periodic_update, args=(self.stop_event,))
        t.setDaemon(True)
        t.start()

    def remove_neighbor(self, id):
        """
        call send_table...() manually
        """
        # print(f'removing {id} from {self.id} ')
        del self.neighbors[id]
        del self.routing_table[id]
        # print('table:', self.routing_table)

    def remove_routs_starting_with(self, node_id):
        """
        except for the starting node it self
        (i.e doesn't remove the neighbor itself)
        NOTE: after using this, call send_table_to_neighbors() manually
        """
        updated = False
        to_remove = []
        for id, info in self.routing_table.items():
            if info[0] == node_id and id != node_id:
                to_remove.append(id)
                updated = True
        for id in to_remove:
            del self.routing_table[id]
        return updated

    def add_update_neighbors(self, node_id, host, port, weight):
        self.neighbors[node_id] = (host, port)
        self.routing_table[node_id] = (node_id, weight)

    def send_data(self, server_host, server_port, data):
        """
        :param server_host: -daa-
        :param server_port: -daa-
        :param data: must be JSON form of one of the data_sharing_protocol s
        :return: nothing
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            try:
                tcp_socket.connect((server_host, server_port))
                tcp_socket.sendall(data)
            except:
                print(f"!!!!!!!!!! error in node {self.id} send_data - server refusing")

            try:
                response = tcp_socket.recv(2048).decode()
                if response:
                    # print(f"received response in node {self.id}:", response)
                    pass
                else:
                    raise socket.error('Client disconnected')
            except:
                print('!!! no response from server !!!')
                return False
            finally:
                tcp_socket.close()

    def send_table_to_neighbors(self):
        data = TableContainer(self.id, self.routing_table).toJSON().encode('UTF-8')
        for neighbor_id, info in self.neighbors.items():
            host = info[0]
            port = info[1]
            # t = threading.Thread(target=self.send_data, args=(host, port, data))
            # t.setDaemon(True)
            # t.start()
            self.send_data(host, port, data)
        self.last_time_table_sent = time.time()

    def update_routing_table(self, neighbor_id, neighbor_table):
        updated = False
        for node_id, info in neighbor_table.items():
            node_id = int(node_id)
            cost = int(info[1])
            cost_to_neighbor = self.routing_table.get(neighbor_id)[1]
            new_cost = cost + cost_to_neighbor
            item = self.routing_table.get(node_id)
            if item is None:
                # there used to be no path to this node
                self.routing_table[node_id] = (self.routing_table[neighbor_id][0], new_cost)
                updated = True
                continue
            current_cost = item[1]

            if new_cost < current_cost:
                self.routing_table[node_id] = (neighbor_id, new_cost)
                updated = True

        if updated:
            self.send_table_to_neighbors()

    def periodic_update(self, stop_event):
        while not stop_event.is_set():
            if not self.has_sent_table_for_once:
                self.send_table_to_neighbors()
                self.has_sent_table_for_once = True
            elif time.time() - self.last_time_table_sent > self.update_period:
                # print(f'periodic update - node {self.id}')
                self.send_table_to_neighbors()

    def client_handler(self, connection):
        """
        just used in listening_server()
        """
        size = 1024 * 2
        while True:
            try:
                data = connection.recv(size)
                if data:
                    dict_data = json.loads(data.decode())
                    print(f"new data received in node {self.id}")
                    self.update_routing_table(int(dict_data['node_id']), dict_data['table'])
                    response = 'OK'.encode('UTF-8')
                    connection.send(response)
                else:
                    raise socket.error('Client disconnected')
            except:
                connection.close()
                return False

    def listening_server(self, stop_event):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((self.host, self.listening_port))
        except:
            print("!!! trouble with socket !!!")
            return

        unaccepted_connections_allowed = 10
        s.listen(unaccepted_connections_allowed)
        print(f"node {self.id} listening on port {self.listening_port} ...")

        while not stop_event.is_set():
            # blocking call, waits to accept a connection
            connection, adrs = s.accept()
            # print("connected to " + adrs[0] + ":" + str(adrs[1]))

            t = threading.Thread(target=self.client_handler, args=(connection,))
            t.setDaemon(True)
            t.start()

        # s.close()
