import socket
import meta_data


def main_process(host, port, request, block_no=None):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_socket:
        tcp_socket.connect((host, port))
        tcp_socket.sendall(request.encode('UTF-8'))

        try:
            data_header = tcp_socket.recv(2048)
        except ConnectionResetError:
            print('connection reset')
            return None
        # print('header:', data_header)

        # expected_data_len = -1
        if len(data_header) > 0:
            # this part of data is string, so it's OK to use decode() for it:
            # (but for image bits, it is not)
            expected_data_len = int(data_header.decode().split("BODY_BYTE_LENGTH: ", 1)[1].strip())
            if block_no == 1:
                meta_data.global_normal_block_size = expected_data_len
        else:
            expected_data_len = \
                meta_data.global_file_size - meta_data.global_num_blocks * meta_data.global_normal_block_size

        # to get all parts of data:
        data_body = tcp_socket.recv(2048)
        while len(data_body) < expected_data_len:
            data_body += tcp_socket.recv(2048)

        # print('data_body:', data_body)

        print('tcp data received' + (' - block #' + str(block_no) if block_no is not None else ''))

        return data_body


def tcp_client_send_req(host, port, request):
    return main_process(host, port, request)


# I've done this due to Python Thread's constraints
def parallel_tcp_client_send_req(host, port, request, results, index):
    res = main_process(host, port, request, index + 1)
    if res is None:
        return None
    else:
        results[index] = res
        return True
