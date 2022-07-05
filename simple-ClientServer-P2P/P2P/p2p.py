import queue
import threading
import time

from ClientServer.tcp_client_send_req import parallel_tcp_client_send_req
from P2P.udp_send_req import udp_send_req
import meta_data


def block_requester(q, ip, port, received_bytes_list, blocks_num):
    while True:
        try:
            work = q.get()
        except queue.Empty:
            print('q empty')
            return
        # don't try to lower this mf or the server will block you:
        time.sleep(2)
        if parallel_tcp_client_send_req(ip, port, 'GET Redsox.jpg:' + str(work) + '\n', received_bytes_list, work) \
                is not None:
            received_data_perc = (blocks_num - received_bytes_list.count(None)) * 100 / blocks_num
            print('received blocks:', received_data_perc, '%')
            q.task_done()
        # print(received_bytes_list)


def p2p_request_file(host, port, request):
    print('sending request for P2P metadata ...')
    num_blocks, file_size, ip1, port1, ip2, port2 = udp_send_req(host, port, request)

    num_blocks = int(num_blocks)
    # the idiots don't actually return the Number of block
    # took me hours to find out
    num_blocks += 1

    file_size = int(file_size)
    port1 = int(port1)
    port2 = int(port2)

    print()
    print('meta data:')
    print('num_blocks:', num_blocks)
    print('file_size:', file_size)
    print('port1:', port1)
    print('port2:', port2)
    print()

    meta_data.global_file_size = file_size
    meta_data.global_num_blocks = num_blocks

    peer_IPs = [ip1, ip2]
    peer_ports = [int(port1), int(port2)]

    to_be_requested_block = 0
    received_bytes_list = [None for _ in range(num_blocks+1)]

    # getting more peer addresses:
    tries = 2
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

    print('\nsending parallel requests for data blocks ...')
    data_block_queue = queue.Queue()
    for i in range(num_blocks+1):
        data_block_queue.put_nowait(i)
    i = 0
    while not data_block_queue.empty():
        t = threading.Thread(target=block_requester,
                             args=(data_block_queue, peer_IPs[i % len(peer_IPs)], peer_ports[i % len(peer_IPs)],
                                   received_bytes_list, num_blocks))
        t.setDaemon(True)
        t.start()

        # don't try to lower this mf or the server will block you:
        time.sleep(2)
        print(' -> threads count:', i+1)
        i += 1

    data_block_queue.join()
    print('\nall data received.')

    print()
    data = received_bytes_list[0]
    for i in range(1, len(received_bytes_list)):
        data = data + received_bytes_list[i]

    return data
