import json
import time

from GraphUtils import inittime_add_update_edge
from model.data_sharing_protocol import TableContainer, EdgeContainer
from model.Node import Node

host = 'localhost'
base_port = 3000

# the topology in the doc:
N = 10
nodes = [None for _ in range(N + 1)]
# 1 based
for i in range(1, N + 1):
    nodes[i] = Node(i, base_port + i, host)

inittime_add_update_edge(nodes[1], nodes[2], 2)
inittime_add_update_edge(nodes[1], nodes[3], 1)
inittime_add_update_edge(nodes[2], nodes[7], 4)
inittime_add_update_edge(nodes[2], nodes[3], 3)
inittime_add_update_edge(nodes[3], nodes[9], 4)
inittime_add_update_edge(nodes[3], nodes[5], 1)
inittime_add_update_edge(nodes[2], nodes[4], 1)
inittime_add_update_edge(nodes[4], nodes[8], 4)
inittime_add_update_edge(nodes[4], nodes[6], 2)
inittime_add_update_edge(nodes[4], nodes[5], 3)
inittime_add_update_edge(nodes[5], nodes[6], 1)
inittime_add_update_edge(nodes[5], nodes[10], 4)

time.sleep(32)
print('##############')
for node in nodes:
    if node is not None:
        # skipping index 0 (the only None)
        print(f"node {node.id} table:", node.routing_table)
