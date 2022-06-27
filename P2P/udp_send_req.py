import socket
import time


def udp_send_req(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_socket:
        udp_socket.connect((host, port))
        udp_socket.sendall(request.encode('UTF-8'))

        # print('receiving data (UDP) ...')

        data_header = udp_socket.recv(2048)
        header_lines = data_header.decode().strip().split("\n")

        udp_socket.close()

    return header_lines[0].split(': ')[1], header_lines[1].split(': ')[1], header_lines[2].split('/')[1], \
           header_lines[3].split(': ')[1], header_lines[4].split('/')[1], header_lines[5].split(': ')[1]
