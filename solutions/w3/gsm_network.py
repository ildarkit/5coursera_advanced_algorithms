# python3


# colors are represented as numbers
COLOURS = range(1, 4)


def varnum(i, j):
    """
    Calculating the variable x_ij for the vertex i of the color j.
    :param i: number of vertex
    :param j: color of vertex
    :return: variable corresponding to the vertex i of the possible color j.
    """
    return (i - 1)*len(COLOURS) + j


def colorable_graph_to_3cnf(vertices, edges):
    """
    Reduction graph coloring problem to 3-cnf sat problem.
    https://research.ijcaonline.org/encc/number1/encc004.pdf
    :param vertices: number of vertices
    :param edges: list of edges
    :return: number of variables and clauses
    """
    # Vertex constraint approach.
    # Color each vertex of a graph G as v_ic in such a way
    # that vertex should have at least one color among available k-colors
    # as follows: v_ic = (v_i1 v v_i2 v v_i3 ... v v_ik)
    clauses = [[varnum(i, j) for j in COLOURS] for i in range(1, vertices + 1)]
    variables = len(COLOURS)*len(clauses)

    # Edges constraint approach.
    # Any edge of a k-colorable graph can be encoded by generating
    # a clause in such a way that two end point of an
    # edge say u,v should not be assigned same color k.
    # The purpose of this approach is to ensure that
    # two adjacent vertex should be assigned different color.
    # e_j = (-u_1 v -v_1) ^ (-u_2 v -v_2) ^ ... ^ (-u_k v -v_k)
    for pair in edges:
        for j in COLOURS:
            clauses.append([-varnum(i, j) for i in pair])
    return variables, clauses


def print_equisatisfiable_sat_formula(vertices, edges):
    """
    This function just prints a satisfiable formula.
    """
    vars, clauses = colorable_graph_to_3cnf(vertices, edges)
    print(len(clauses), vars, sep=' ')
    for clause in clauses:
        print(' '.join(map(str, clause)), end=' 0\n')


if __name__ == '__main__':
    n, m = map(int, input().split())
    edges = [list(map(int, input().split())) for _ in range(m)]
    print_equisatisfiable_sat_formula(n, edges)
