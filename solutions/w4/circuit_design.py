# python3


DEBUG = False


class ImplicationGraph:
    def __init__(self, _2sat):
        self._2sat = _2sat
        self.adjacency = dict()
        self.reversed_adjacency = dict()

    def build(self):
        for i, j in self._2sat:
            self.add_edges([(-i, j), (-j, i)], self.adjacency)
            self.add_edges([(j, -i), (i, -j)], self.reversed_adjacency)

    @staticmethod
    def add_edges(edges, adj):
        for i, j in edges:
            if i in adj:
                adj[i].append(j)
            else:
                adj[i] = [j]

    @property
    def adjacency_graph(self):
        return self.adjacency

    @property
    def reversed_adjacency_graph(self):
        return self.reversed_adjacency


def is_satisfiable(number_variables, clauses):
    sat_assignment = None
    implication_graph = ImplicationGraph(clauses)
    implication_graph.build()
    scc = find_scc(implication_graph.adjacency_graph,
                   implication_graph.reversed_adjacency_graph)
    if scc:
        sat_assignment = [None]*number_variables
        i = 0
        for s in reversed(scc):
            if i == number_variables:
                break
            i += 1
            for v in s:
                sat_assignment[abs(v) - 1] = 1 if v > 0 else 0
    return sat_assignment


def find_scc(graph, reversed_graph):
    scc = []
    visited = dict()
    reversed_visited = dict()
    post_order = []
    dfs(reversed_graph, reversed_visited, post_order)
    for v in reversed(post_order):
        scc.append(dict())
        if v not in visited:
            sat = explore(graph, visited, v, scc)
            if not sat:
                return None
    return scc


def dfs(graph, visited, post_order):
    for v in graph:
        explore(graph, visited, v, post_order=post_order)


def explore(graph, visited, v, scc=None, sat=True, post_order=None):
    if v in visited:
        return
    visited[v] = 1
    for w in graph.get(v, ()):
        if w not in visited:
            sat = explore(graph, visited, w, scc, sat, post_order)
            if not sat:
                return sat
    if scc:
        scc[-1][v] = v
    if not sat or (scc and -v in scc[-1]):
        if DEBUG:
            print('(DEBUG) v and -v in same scc: v = {}'.format(v))
            print('(DEBUG) SCCs = {}'.format(scc))
        return False
    if post_order is not None:
        post_order.append(v)
    return sat


if __name__ == '__main__':
    n, m = map(int, input().split())
    clauses = [list(map(int, input().split())) for _ in range(m)]
    result = is_satisfiable(n, clauses)
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
