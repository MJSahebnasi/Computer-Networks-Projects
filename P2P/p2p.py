import queue
import threading
import time
from threading import Thread

from ClientServer.tcp_client_send_req import parallel_tcp_client_send_req
from P2P.udp_send_req import udp_send_req


def block_requester(q, ip, port, received_bytes_list):
    while True:
        try:
            work = q.get()
        except queue.Empty:
            return
        time.sleep(2)
        parallel_tcp_client_send_req(ip, port, 'GET Redsox.jpg:' + str(work) + '\n', received_bytes_list, work - 1)
        q.task_done()
        print(received_bytes_list)


def p2p_request_file(host, port, request):
    print('sending request for P2P metadata ...')
    num_blocks, file_size, ip1, port1, ip2, port2 = udp_send_req(host, port, request)

    num_blocks = int(num_blocks)
    file_size = int(file_size)
    port1 = int(port1)
    port2 = int(port2)

    peer_IPs = [ip1, ip2]
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
        _, _, ip1, port1, ip2, port2 = udp_send_req(host, port, request)
        if ip1 not in peer_IPs and port1 not in peer_ports:
            peer_IPs.append(ip1)
            peer_ports.append(port1)
        if ip2 not in peer_IPs and port2 not in peer_ports:
            peer_IPs.append(ip2)
            peer_ports.append(port2)

    print('peer addresses achieved (IP,port):', [adr for adr in zip(peer_IPs, peer_ports)])

    print('sending parallel requests for data blocks ...')

    # # # attempt 1: failed (tcp connections kept getting closed) #
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

    # # # attempt2:
    data_block_queue = queue.Queue()
    for i in range(1, num_blocks + 1):
        data_block_queue.put_nowait(i)
    for i in range(len(peer_IPs)):
        threading.Thread(target=block_requester,
                         args=(data_block_queue, peer_IPs[i], peer_ports[i], received_bytes_list)).start()
    data_block_queue.join()
    print('all data received.')

    print()
    data = received_bytes_list[0]
    for i in range(1, len(received_bytes_list)):
        data = data + received_bytes_list[i]

    return data
