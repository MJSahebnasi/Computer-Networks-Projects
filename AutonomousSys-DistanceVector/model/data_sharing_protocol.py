import json


class JSONable:
    def toJSON(self):
        return json.dumps(self.__dict__)


class TableContainer(JSONable):
    """
    for sharing routing_table on the network
    """

    def __init__(self, node_id, table):
        self.node_id = node_id
        self.table = table


class EdgeContainer(JSONable):
    def __init__(self, node_id, new_weight):
        """
        for announcing edge change on the network
        when sending on the network AND in the destination, this obj will be converted to dict
        the purpose of using this when sending data is to reduce the chance of making mistakes
        :param node_id: -daa-
        :param new_weight: None: edge removed, O.W: edge weight updated OR new edge created
        """
        self.node_id = node_id
        self.new_weight = new_weight
