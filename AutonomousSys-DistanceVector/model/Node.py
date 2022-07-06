import socket
import threading
import selectors
import types


class Node:
    """
    After init, neighbors and routing_table are not set.
    Just use add_update_neighbor(). The routing_table will automatically be updated.
    """

    def __init__(self, id, listening_port, sending_port, host):
        self.id = id
        self.listening_port = listening_port
        self.sending_port = sending_port
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

    def listening_server(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except:
            print("!!! Could not create socket !!!")
            return

        print("[-] Socket Created")

        # bind socket
        try:
            s.bind((self.host, self.listening_port))
            print("[-] Socket Bound to port " + str(self.listening_port))
        except:
            print("!!! Bind Failed !!!")
            return

        s.listen(10)
        print(f"node {self.id} listening on port {self.listening_port} ...")

        def client_handler(connection):
            while True:
                data = connection.recv(1024 * 2)
                if not data:
                    break
                reply = "OK"
                connection.sendall(reply)

            print(f"data received in node {self.id} server:", data)

            connection.close()

        while True:
            # blocking call, waits to accept a connection
            connection, adrs = s.accept()
            print("[-] Connected to " + adrs[0] + ":" + str(adrs[1]))

            t = threading.Thread(target=client_handler, args=(connection,))
            t.setDaemon(True)
            t.start()

        s.close()

    def send_data(self, server_host, server_port, data):
        """
        <data> must be JSON
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
            tcp_socket.connect((server_host, server_port))
            tcp_socket.sendall(data)

            try:
                response = tcp_socket.recv(2048)
            except:
                print('!!! no response from server !!!')
                return None

            print('response:', response)
