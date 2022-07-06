import json
import time

from model.Node import Node

host = 'localhost'
data = {'table': {'a': 1, 'b': 2}}
bytes_data = json.dumps(data).encode('UTF-8')
n1 = Node(1, 3000, host)
n2 = Node(2, 3001, host)
n3 = Node(3, 3002, host)
n4 = Node(4, 3003, host)
print('--------')
n2.send_data(host, 3002, bytes_data)
n1.send_data(host, 3002, bytes_data)
n4.send_data(host, 3002, bytes_data)
# print(type(json.dumps(data).encode('UTF-8')))
