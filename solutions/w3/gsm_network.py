# python3


COLOURS = range(1, 4)


def varnum(i, j):
    return (i - 1)*len(COLOURS) + j


def colorable_graph_to_3cnf(vertices, edges):
    clauses = [[varnum(i, j) for j in COLOURS] for i in range(1, vertices + 1)]
    variables = len(COLOURS)*len(clauses)

    for pair in edges:
        for j in COLOURS:
            clauses.append([-varnum(i, j) for i in pair])
    return variables, clauses


def print_equisatisfiable_sat_formula(vertices, edges):
    """
    This solution prints a simple satisfiable formula
    and passes about half of the tests.
    Change this function to solve the problem.
    :return:
    """
    vars, clauses = colorable_graph_to_3cnf(vertices, edges)
    print(len(clauses), vars, sep=' ')
    for clause in clauses:
        print(' '.join(map(str, clause)), end=' 0\n')


if __name__ == '__main__':
    n, m = map(int, input().split())
    edges = [list(map(int, input().split())) for _ in range(m)]
    print_equisatisfiable_sat_formula(n, edges)
