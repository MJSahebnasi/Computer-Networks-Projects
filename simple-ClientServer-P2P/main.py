import time

from ClientServer.tcp_client_send_req import tcp_client_send_req
from P2P.p2p import p2p_request_file
from P2P.udp_send_req import udp_send_req

# print('----- CS-tcp: ')
# hostname_1 = 'plum.cs.umass.edu'
hostname_2 = 'pear.cs.umass.edu'
# cs_port = 18765
#
# print('sending request ...')
# t1 = time.time()
# cs_data = tcp_client_send_req(hostname_2, cs_port, 'GET Redsox.jpg \n')
# t2 = time.time()
# print('all data received in', t2-t1, 's')
# # # writing on file:
# f = open("cs_received_data.jpg", "wb")
# f. write(cs_data)
# f. close()
# print('data written on file.')

print('----- P2P: ')
p2p_port = 19876
p2p_data = p2p_request_file(hostname_2, p2p_port, 'GET Redsox.jpg.torrent')
# writing on file:
f = open("p2p_received_image.jpg", "wb")
f. write(p2p_data)
f. close()
print('data written on file.')


