# python3


INF = 100000


class Edge:
    def __init__(self, u, v):
        self.u = u
        self.v = v
        self.visited = False


def read_data():
    n, m = map(int, input().split())
    adj_matrix = [list(map(int, input().split())) for i in range(n)]
    return adj_matrix


def write_response(matching):
    line = [str(-1 if x == -1 else x) for x in matching]
    print(' '.join(line))


def build_network(adj_matrix):
    adj_network = [{} for _ in range(len(adj_matrix) + len(adj_matrix[0]) + 2)]
    adj_network[0] = {i + 1: Edge(0, i + 1) for i in range(len(adj_matrix))}
    edges_count = 0
    # count_unlinked_nodes = list(map(sum, zip(*adj_matrix))).count(0)
    # nodes_count = len(adj_matrix[0]) - count_unlinked_nodes + 2 + len(adj_matrix)
    edges_from_nodes = set()
    for i in range(len(adj_matrix)):
        for j in range(len(adj_matrix[i])):
            if adj_matrix[i][j] == 1:
                edge = Edge(i + 1, j + 1 + len(adj_matrix))
                adj_network[i + 1].update({j + 1 + len(adj_matrix): edge})
                edges_from_nodes.add(j + 1 + len(adj_matrix))
                edges_count += 1
    for i in edges_from_nodes:
        adj_network[i].update({len(adj_network) - 1: Edge(i, len(adj_network) - 1)})
    return adj_network, edges_count


def find_matching(graph, from_, to, edge_count):
    """
    Implementation of the Edmonds-Karp algorithm for
    searching max flow.
    :param graph: directed graph
    :param from_: node S
    :param to: node T
    :return: max flow
    """
    result = [-1 for _ in range(len(graph[0]))]
    max_count = 0
    while edge_count > max_count:
        counter = 0
        crew_flights = [-1 for _ in range(len(graph[0]))]
        save_prevs = []
        while True:
            prev = find_augmenting_path(graph, from_, to)
            if prev[to] == -1:
                break
            u = to
            crew = -1
            while u != from_:
                v = prev[u]
                if crew == -1:
                    crew = v
                elif v > 0:
                    crew_flights[v - 1] = crew - len(crew_flights)
                    counter += 1
                edge = graph[v][u]
                edge.visited = True
                u = v
            save_prevs.append(prev)

        edge_count -= counter
        if max_count < counter:
            max_count = counter
            result = crew_flights

        for save_prev in save_prevs:
            u = to
            while u != from_:
                v = save_prev[u]
                edge = graph[v][u]
                if edge.u == from_ or edge.v == to:
                    edge.visited = False
                u = v

    return result


def find_augmenting_path(graph, from_, to):
    """
    Search for a augmenting path by traversing the graph in depth (DFS).
    :param graph: directed graph
    :param from_: node S
    :param to: node T
    :return: list of edges and list of flows of vertices
    """
    stack = [from_]
    prev = [-1 for _ in range(len(graph))]
    while stack:
        vertex_id = stack.pop()
        for v in graph[vertex_id]:
            adj_edge = graph[vertex_id][v]
            if not adj_edge.visited and prev[v] == -1:
                stack.append(v)
                prev[v] = vertex_id
            if adj_edge.v == to:
                # node T has been reached
                # stop search for a augmenting path
                stack = []
                break
    return prev


if __name__ == '__main__':
    adj_matrix = read_data()
    adj_network, edge_count = build_network(adj_matrix)
    matching = find_matching(adj_network, 0, len(adj_network) - 1, edge_count)
    write_response(matching)
