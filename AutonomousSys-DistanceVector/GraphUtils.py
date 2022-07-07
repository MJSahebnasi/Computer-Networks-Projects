from model.Node import Node


def find_node_by_id(nodes, id):
    for node in nodes:
        if node is None:
            # first element
            continue
        if node.id == id:
            return node
    return None


def inittime_add_update_edge(node1, node2, weight):
    """
    for init time: won't send data on the network
    """
    node1.add_update_neighbors(node2.id, node2.host, node2.listening_port, weight)
    node2.add_update_neighbors(node1.id, node1.host, node1.listening_port, weight)


def extract_path(nodes, start_node, dest_node, path):
    """
    :param nodes: list of all nodes
    :param start_node: a Node object
    :param dest_node: a Node object
    :return: nodes in the shortest path from start_node to dest_node
    """
    current_node = start_node
    next_node_id = current_node.routing_table.get(dest_node.id)[0]
    if not next_node_id:
        print('---false----')
        # no path
        return False
    next_node = find_node_by_id(nodes, next_node_id)

    if next_node.id == dest_node.id:
        # destination reached
        path.append(dest_node.id)
        return True

    path.append(next_node.id)
    return extract_path(nodes, next_node, dest_node, path)


def update_link(node1, node2, new_weight):
    """
    :param node1: a Node object
    :param node2: a Node object
    :param new_weight: -daa-
    :return: nothing
    """
    # TODO
    # update edges (in neighbors list)
    # update routing_tables, how?
    # notify neighbor nodes: through network
    pass


def add_node(nodes, id, port, host, neighbor_id_s, weights):
    """
    use it like this:
    my_nodes.append(add_node(...))
    :param id: new node's id
    :param port: -daa-
    :param host: -daa-
    :param neighbor_id_s: -daa- 
    :param weights: -daa-
    :return: the newly created host
    """
    new_node = Node(id, port, host)
    for i in range(len(neighbor_id_s)):
        neighbor = find_node_by_id(nodes, neighbor_id_s[i])
        inittime_add_update_edge(new_node, neighbor, weights[i])
        neighbor.send_table_to_neighbors()
    new_node.send_table_to_neighbors()
    return new_node


def remove_node(node):
    # TODO
    # update neighbors through network
    pass
