
class DAGNode:
    def __init__(self):
        self.edges = []
        self.in_edges = []

    def get_short_name(self):
        return self.short_name

    def get_edges(self):
        return self.edges

    def add_edge(self, edge):
        if edge.get_source() != self:
            logger.warning('Bad edge registration, source node does not match.')
        else:
            self.edges.append(edge)

    def register_as_target_of_edge(self, edge):
        self.in_edges.append(edge)

    def get_parents(self):
        return [edge.source for edge in self.in_edges]

class DAGEdge:
    def get_source(self):
        return self.source

    def get_target(self):
        return self.target
