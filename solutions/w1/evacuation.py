# python3


INF = 100000


class Edge:
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0


class FlowGraph:
    """
    This class implements a bit unusual scheme for storing edges of the graph,
    in order to retrieve the backward edge for a given edge quickly.
    """
    def __init__(self, n):
        # List of all - forward and backward - edges
        self.edges = []
        # These adjacency lists store only indices of edges in the edges list
        self.graph = [[] for _ in range(n)]

    def add_edge(self, from_, to, capacity):
        # Note that we first append a forward edge and then a backward edge,
        # so all forward edges are stored at even indices (starting from 0),
        # whereas backward edges are stored at odd indices.
        forward_edge = Edge(from_, to, capacity)
        backward_edge = Edge(to, from_, 0)
        self.graph[from_].append(len(self.edges))
        self.edges.append(forward_edge)
        self.graph[to].append(len(self.edges))
        self.edges.append(backward_edge)

    def size(self):
        return len(self.graph)

    def get_ids(self, from_):
        return self.graph[from_]

    def get_edge(self, id):
        return self.edges[id]

    def add_flow(self, id, flow):
        # To get a backward edge for a true forward edge (i.e id is even), we should get id + 1
        # due to the described above scheme. On the other hand, when we have to get a "backward"
        # edge for a backward edge (i.e. get a forward edge for backward - id is odd), id - 1
        # should be taken.
        #
        # It turns out that id ^ 1 works for both cases. Think this through!
        self.edges[id].flow += flow
        self.edges[id ^ 1].flow -= flow


def read_data():
    vertex_count, edge_count = map(int, input().split())
    graph = FlowGraph(vertex_count)
    for _ in range(edge_count):
        u, v, capacity = map(int, input().split())
        graph.add_edge(u - 1, v - 1, capacity)
    return graph


def max_flow(graph, from_, to):
    """
    Implementation of the Edmonds-Karp algorithm for
    searching max flow.
    :param graph: directed graph
    :param from_: node S
    :param to: node T
    :return: max flow
    """
    flow = 0
    # your code goes here
    while True:
        prev, h = find_augmenting_path(graph, from_, to)
        if h[to] == INF:
            break
        flow += h[to]
        u = INF
        while u != from_:
            edge_id = prev.pop()
            edge = graph.get_edge(edge_id)
            if edge.v == u or u == INF:
                u = edge.u
                graph.add_flow(edge_id, h[to])
    return flow


def find_augmenting_path(graph, from_, to):
    """
    Search for a augmenting path by traversing the graph in width (BFS).
    :param graph: directed graph
    :param from_: node S
    :param to: node T
    :return: list of edges and list of flows of vertices
    """
    queue = [from_]
    prev = []
    h = [INF for _ in range(graph.size())]
    while queue and h[to] == INF:
        vertex_id = queue.pop(0)
        for adj in graph.get_ids(vertex_id):
            adj_edge = graph.get_edge(adj)
            if h[adj_edge.v] == INF:
                if adj_edge.capacity > adj_edge.flow:
                    h[adj_edge.v] = min(h[vertex_id], adj_edge.capacity - adj_edge.flow)
                    queue.append(adj_edge.v)
                    prev.append(adj)
            if h[to] < INF:
                # node T has been reached
                # stop search for a augmenting path
                break
    return prev, h


if __name__ == '__main__':
    graph = read_data()
    print(max_flow(graph, 0, graph.size() - 1))
