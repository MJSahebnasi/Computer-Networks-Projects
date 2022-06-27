import time
from threading import Thread

from ClientServer.tcp_client_send_req import parallel_tcp_client_send_req
from P2P.udp_send_req import udp_send_req


def p2p_request_file(host, port, request):
    print('sending request for P2P metadata ...')
    num_blocks, file_size, IP1, port1, IP2, port2 = udp_send_req(host, port, request)

    num_blocks = int(num_blocks)
    file_size = int(file_size)
    port1 = int(port1)
    port2 = int(port2)

    peer_IPs = [IP1, IP2]
    peer_ports = [int(port1), int(port2)]

    to_be_requested_block = 1
    received_bytes_list = [None for i in range(num_blocks)]

    # getting more peer addresses:
    tries = 1
    for i in range(tries):
        # this 2s delay is achieved by trial and error:
        # (smaller values will lead to being blocked by the server)
        time.sleep(2)
        print('getting more peer addresses ...')
        _, _, IP1, port1, IP2, port2 = udp_send_req(host, port, request)
        if IP1 not in peer_IPs and port1 not in peer_ports:
            peer_IPs.append(IP1)
            peer_ports.append(port1)
        if IP2 not in peer_IPs and port2 not in peer_ports:
            peer_IPs.append(IP2)
            peer_ports.append(port2)

    # i = 0
    # while to_be_requested_block <= num_blocks:
    #     time.sleep(2)
    #     ip = peer_IPs[i]
    #     port = peer_ports[i]
    #     thread = Thread(target=parallel_tcp_client_send_req,
    #                     args=(ip, port, 'GET Redsox.jpg:' + str(to_be_requested_block), received_bytes_list,
    #                           to_be_requested_block - 1))
    #     print('block', to_be_requested_block, 'requested')
    #     print(received_bytes_list)
    #     to_be_requested_block += 1
    #     thread.start()
    #     i = (i + 1) % len(peer_IPs)

    print('peer addresses achieved (IP,port):', [adr for adr in zip(peer_IPs, peer_ports)])
    print('all data received.')

    print()
    data = received_bytes_list[0]
    for i in range(1, len(received_bytes_list)):
        data = data + received_bytes_list[i]

    return data
