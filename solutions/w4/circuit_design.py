# python3
import sys
import threading


DEBUG = False


class ImplicationGraph:
    """
    For a 2-CNF formula, its implication graph is constructed as follows:
    - for each variable x, introduce 2 vertices labeled by x and -x
    - for each 2-clause (l1 V l2), introduce 2 directed edges -l1 -> l2 and -l2 -> l1
    - for each 1-clause (l1), introduce an edge -l1 -> l1.
    For example clause (-x V y) introduce edges x -> y and -y -> -x.
    """
    def __init__(self, _2sat):
        self._2sat = _2sat
        self.adjacency = dict()
        self.reversed_adjacency = dict()

    def build(self):
        # constructing direct and reverse implication graphs
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
    """
    The implementation of the algorithm for solving
    the 2-satisfiability problem presented in the 2-cnf formula.
    The problem of 2-satisfiability is to assign values (0 or 1)
    to variables so that the formula is true.
    That is, to answer the question: is there such a set of variables
    on which the formula takes its true value?
    The 2-sat problem is solved in polynomial time.
    :param number_variables:
    :param clauses:
    :return: boolean assignment or None
    """
    sat_assignment = None
    implication_graph = ImplicationGraph(clauses)
    implication_graph.build()
    scc = find_scc(implication_graph.adjacency_graph,
                   implication_graph.reversed_adjacency_graph)
    if scc:
        sat_assignment = [None]*number_variables
        for s in reversed(scc):
            for v in s:
                sat_assignment[abs(v) - 1] = 1 if v > 0 else 0
    return sat_assignment


def find_scc(graph, reversed_graph):
    """
    Search SCC in the reversed directed graph.
    1) All variables lying in the same SCC of
    the implication graph should be assigned the same value.
    2) In particular, if a SCC contains a variable together with its negation,
    then the formula is unsatisfiable.
    3) It turns out that otherwise the formula is satisfiable!
    :param graph:
    :param reversed_graph:
    :return: list of SCC
    """
    scc = []
    visited = dict()
    reversed_visited = dict()
    post_order = []
    dfs(reversed_graph, reversed_visited, post_order)
    for v in reversed(post_order):
        if v not in visited:
            scc.append(dict())
            sat = explore(graph, visited, v, scc)
            if not sat:
                return None
    return scc


def dfs(graph, visited, post_order):
    """
    Traversing all vertices of the graph in depth.
    :param graph: graph
    :param visited: visited vertexes
    :param post_order: list of post ordered vertexes
    """
    for v in graph:
        explore(graph, visited, v, post_order=post_order)


def explore(graph, visited, v, scc=None, is_satisfy=True, post_order=None):
    """
    Recursive traversal of the adjacent vertexes of the vertex "v" of the directed graph.
    :param graph: graph
    :param visited: visited vertexes
    :param v: current vertex
    :param scc: list of strongly connected component
    :param is_satisfy:
    :param post_order: list of post ordered vertexes
    :return:
    """
    if v in visited:
        return
    visited[v] = 1
    for w in graph.get(v, ()):
        if w not in visited:
            is_satisfy = explore(graph, visited, w, scc, is_satisfy, post_order)
            if not is_satisfy:
                return is_satisfy
    if scc:
        # add vertex "v" to the current SCC
        scc[-1][v] = v
    if not is_satisfy or (scc and -v in scc[-1]):
        # If the same SCC contain both "v" and "-v" vertices
        # then 2-sat is falsified.
        # Answer is "UNSATISFIABLE".
        if DEBUG:
            print('(DEBUG) v and -v in same scc: v = {}'.format(v))
            print('(DEBUG) SCCs = {}'.format(scc))
        return False
    if post_order is not None:
        post_order.append(v)
    return is_satisfy


def main():
    # this function is executed in the thread
    n, m = map(int, input().split())
    clauses = [list(map(int, input().split())) for _ in range(m)]
    result = is_satisfiable(n, clauses)
    if result is None:
        print("UNSATISFIABLE")
    else:
        print("SATISFIABLE")
        print(" ".join(str(i if result[i - 1] else -i) for i in range(1, n + 1)))


if __name__ == '__main__':
    # This code is used to avoid stack overflow issues
    sys.setrecursionlimit(10 ** 6)  # max depth of recursion
    threading.stack_size(2 ** 26)  # new thread will get stack of such size
    t = threading.Thread(target=main)
    t.start()
    t.join()

