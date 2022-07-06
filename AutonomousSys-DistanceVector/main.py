import json
import time

from GraphUtils import inittime_add_update_edge
from model.data_sharing_protocol import TableContainer, EdgeContainer
from model.Node import Node

host = 'localhost'
n1 = Node(1, 3001, host)
n2 = Node(2, 3002, host)
n3 = Node(3, 3003, host)
n4 = Node(4, 3004, host)
n5 = Node(5, 3005, host)

inittime_add_update_edge(n1, n2, 9)
inittime_add_update_edge(n1, n3, 1)
inittime_add_update_edge(n1, n4, 2)
inittime_add_update_edge(n2, n3, 2)
inittime_add_update_edge(n2, n5, 4)
inittime_add_update_edge(n4, n5, 4)

time.sleep(15)
print('##############')
print(n1.routing_table)
print(n2.routing_table)
print(n3.routing_table)
print(n4.routing_table)
print(n5.routing_table)
# while not input("-1 for exit: ") == -1:
#     pass
###########
# dic = {'a': ('A', 10), 'b': ('B', 20)}
# print(dic)
# print([i for i in dic.values()])
# print(type([dic.values()]))
# print(dic.keys())
# print(type(dic.keys()))
# for k, v in dic.items():
#     print(k, v[0])
# a = dic.get('z')
# print(a)
###################
# t = TableContainer(1, dic).toJSON().encode('UTF-8')
# t2 = json.loads(t.decode())
# print(t2)
# t = TableContainer(1, dic)
# s = json.dumps(t)
# s = t.toJSON()
# print(s)
# t2 = json.loads(s)
# print(type(t2))
