def inittime_add_update_edge(node1, node2, weight):
    """
    for init time: won't send data on the network
    """
    node1.add_update_neighbors(node2.id, node2.host, node2.listening_port, weight)
    node2.add_update_neighbors(node1.id, node1.host, node1.listening_port, weight)

def extract_path(start_node, dest_node):
    """
    :param start_node: a Node object
    :param dest_node: a Node object
    :return: nodes in the shortest path from start_node to dest_node
    """
    pass
    # TODO


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


def add_node(node_id, edges):
    # TODO update parameters
    """
    use it like this:
    my_nodes.append(add_node(...))

    :param node_id: -daa-
    :param edges: list of (other_node, weight) pairs
    :return: the newly created node
    """

    # TODO notify neighbors through network


def remove_node(node):
    # TODO
    # update neighbors through network
    pass
