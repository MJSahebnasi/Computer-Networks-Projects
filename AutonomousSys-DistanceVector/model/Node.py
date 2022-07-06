import socket
import threading


class Node:
    """
    After init, neighbors and routing_table are not set.
    Just use add_update_neighbor(). The routing_table will automatically be updated.
    """

    def __init__(self, id, listening_port, host):
        self.id = id
        self.listening_port = listening_port
        self.host = host

        self.neighbors = []
        # contains (node_id, weight) pairs

        self.routing_table = {self.id: (None, 0)}
        # contains {node_id: (next_node_id, path_cost)} key-value pairs
        # next_node_id determines the next node to see when routing to the node (with node_id)

        t = threading.Thread(target=self.listening_server)
        t.setDaemon(True)
        t.start()

    def add_update_neighbor(self, node_id, weight):
        self.neighbors.append(node_id)
        self.routing_table[node_id] = (node_id, weight)

    def client_handler(self, connection):
        """
        just used in listening_server()
        """
        size = 1024 * 2
        while True:
            try:
                data = connection.recv(size)
                if data:
                    print(f"received data in node {self.id}:", data)
                    response = 'OK'.encode('UTF-8')
                    connection.send(response)
                else:
                    raise socket.error('Client disconnected')
            except:
                connection.close()
                return False

    def listening_server(self):
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

        while True:
            # blocking call, waits to accept a connection
            connection, adrs = s.accept()
            # print("connected to " + adrs[0] + ":" + str(adrs[1]))

            t = threading.Thread(target=self.client_handler, args=(connection,))
            t.setDaemon(True)
            t.start()

        # s.close()

    def send_data(self, server_host, server_port, data):
        """
        <data> must be JSON
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((server_host, server_port))
            tcp_socket.sendall(data)

            print(f'data sent to server from node {self.id}')

            try:
                response = tcp_socket.recv(2048).decode()
                if response:
                    print(f"received response in node {self.id}:", response)
                else:
                    raise socket.error('Client disconnected')
            except:
                print('!!! no response from server !!!')
                return False
            finally:
                tcp_socket.close()
