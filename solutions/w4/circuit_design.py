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


if __name__ == '__main__':
    n, m = map(int, input().split())
    clauses = [list(map(int, input().split())) for _ in range(m)]
    result = is_satisfiable(clauses)
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(" ".join(str(-i-1 if result[i] else i+1) for i in range(n)))
