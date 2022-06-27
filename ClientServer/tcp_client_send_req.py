import socket


def tcp_client_send_req(host, port, request):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        s.sendall(b"GET Redsox.jpg \n")
        # s.sendall(request.encode('UTF-8'))
        data = s.recv(1024)

    decoded_data = data.decode()
    print(data)
    print(decoded_data)

    return data
