from GraphUtils import extract_path, find_node_by_id, add_node


def help(valid_commands):
    print('valid command patterns:')
    for s in valid_commands:
        print("\r", s)
    print('--------------')


def program(nodes):
    valid_commands = [
        "shortest_path node1_id node2_id",
        "routing_table node_id",
        "modify_link node1_id node2_id weight",
        "add_node id port host node2_id w2 node3_id w3 ...",
        "remove_node node_id",
        "exit",
        "help"
    ]

    print('--------------')
    help(valid_commands)

    while True:
        cmnd = input(" -> ")

        cmnd_parts = cmnd.strip().split(' ')

        if cmnd_parts[0] == "exit":
            return
        elif cmnd_parts[0] == "help":
            help(valid_commands)
        elif cmnd_parts[0] == "routing_table":
            id = int(cmnd_parts[1])
            node = find_node_by_id(nodes, id)
            print(f"for node {id}: (destination node: (next node, cost))")
            print(node.routing_table)
        elif cmnd_parts[0] == "shortest_path":
            node1 = find_node_by_id(nodes, int(cmnd_parts[1]))
            node2 = find_node_by_id(nodes, int(cmnd_parts[2]))
            path = [node1.id]
            res = extract_path(nodes, node1, node2, path)
            if res:
                print('path:', path)
            else:
                print('there is no path')
        elif cmnd_parts[0] == "add_node":
            id = int(cmnd_parts[1])
            port = int(cmnd_parts[2])
            host = cmnd_parts[3]
            neighbor_id_s = []
            weights = []
            for i in range(4, len(cmnd_parts), 2):
                neighbor_id_s.append(int(cmnd_parts[i]))
                weights.append(int(cmnd_parts[i + 1]))
            new_node = add_node(nodes, id, port, host, neighbor_id_s, weights)
            nodes.append(new_node)
        elif cmnd_parts[0] == "remove_node":
            id = int(cmnd_parts[1])
            node = find_node_by_id(nodes, id)
            for neighbor_id, _ in node.neighbors:
                neighbor = find_node_by_id(nodes, neighbor_id)
                neighbor.remove_neighbor(id)
            nodes = [n for n in nodes if n.id != id]
        elif cmnd_parts[0] == "modify_link":
            id1 = int(cmnd_parts[1])
            id2 = int(cmnd_parts[2])
            w = int(cmnd_parts[3])
            node1 = find_node_by_id(nodes, id1)
            node2 = find_node_by_id(nodes, id2)

            node1.add_update_neighbors(node2.id, node2.host, node2.listening_port, w)
            node2.add_update_neighbors(node1.id, node1.host, node1.listening_port, w)

            node1.send_table_to_neighbors()
            node2.send_table_to_neighbors()
        else:
            print('invalid command')
