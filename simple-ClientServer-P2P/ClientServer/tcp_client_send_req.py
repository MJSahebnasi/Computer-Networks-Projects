import socket


def main_process(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((host, port))
        tcp_socket.sendall(request.encode('UTF-8'))

        data_header = tcp_socket.recv(2048)
        print('tcp data received')

        # this part of data is string, so it's OK to use decode() for it:
        # (but for image bits, it is not)
        expected_data_len = int(data_header.decode().split("BODY_BYTE_LENGTH: ", 1)[1].strip())

        # to get all parts of data:
        data_body = tcp_socket.recv(2048)
        while len(data_body) < expected_data_len:
            data_body += tcp_socket.recv(2048)

    return data_body


def tcp_client_send_req(host, port, request):
    return main_process(host, port, request)


# I've done this due to Python Thread's constraints
def parallel_tcp_client_send_req(host, port, request, results, index):
    results[index] = main_process(host, port, request)
