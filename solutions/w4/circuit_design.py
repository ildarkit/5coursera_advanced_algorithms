# python3


class ImplicationGraph:
    def __init__(self, _2sat):
        self._2sat = _2sat
        self.adjacency = dict()
        self.reversed_adjacency = dict()

    def build(self):
        for i, j in self._2sat:
            self.add_2edges([(-i, j), (-j, i)], self.adjacency)
            self.add_2edges([(i, -j), (j, -i)], self.reversed_adjacency)

    @staticmethod
    def add_2edges(edges, adj):
        for i, j in edges:
            if i in adj:
                adj[i].append(j)
            else:
                adj[i] = [j]
            if j in adj:
                adj[j].append(i)
            else:
                adj[j] = [i]

    @property
    def adjacency_graph(self):
        return self.adjacency

    @property
    def reversed_adjacency_graph(self):
        return self.reversed_adjacency


def is_satisfiable(clauses):
    sat_assingment = None
    implication_graph = ImplicationGraph(clauses)
    implication_graph.build()
    scc = find_scc(implication_graph.adjacency_graph,
                   implication_graph.reversed_adjacency_graph)
    if scc:
        for c in reversed(scc):
            pass
    return sat_assingment


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
    pass


def explore(graph, visited, v, scc, sat=True):
    visited[v] = 1
    scc[-1][v] = v
    if not sat or -v in scc[-1]:
        return False
    for w in graph[v]:
        if w not in visited:
            sat = explore(graph, visited, w, scc, sat)
            if not sat:
                return sat
    return sat


if __name__ == '__main__':
    n, m = map(int, input().split())
    clauses = [list(map(int, input().split())) for _ in range(m)]
    result = is_satisfiable(clauses)
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
