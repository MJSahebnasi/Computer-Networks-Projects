class Node:
    """
    After init, neighbors and routing_table are not set.
    Just use add_update_neighbor(). The routing_table will automatically be updated.
    """
    def __init__(self, id):
        self.id = id

        self.neighbors = []
        # contains (node_id, weight) pairs

        self.routing_table = {self.id: (None, 0)}
        # contains {node_id: (next_node_id, path_cost)} key-value pairs
        # next_node_id determines the next node to see when routing to the node (with node_id)

    def add_update_neighbor(self, node_id, weight):
        self.neighbors.append(node_id)
        self.routing_table[node_id] = (node_id, weight)


