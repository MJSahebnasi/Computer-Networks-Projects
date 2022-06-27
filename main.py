from ClientServer.tcp_client_send_req import tcp_client_send_req

print('----- tcp request: ')
cs_hostname_1 = 'plum.cs.umass.edu'
cs_hostname_2 = 'pear.cs.umass.edu'
cs_port = 18765

cs_data = tcp_client_send_req(cs_hostname_2, cs_port, 'GET Redsox.jpg \n')
f = open("cs_data.txt", "wb")
f. write(cs_data)
f. close()
