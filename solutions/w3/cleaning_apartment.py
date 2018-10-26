# python3
import itertools


def varnum(i, j, lenght):
    """
    Calculating the variable x_ij for the vertex i of the color j.
    :param i: number of vertex
    :param j: color of vertex
    :return: variable corresponding to the vertex i of the possible color j.
    """
    return (i - 1)*lenght + j


def print_equisatisfiable_sat_formula(vertices, edges):
    """
    This solution prints a satisfiable formula.
    """
    clauses = hamiltonian_path_to_sat(vertices, edges)
    variables = vertices * vertices
    print(len(clauses), variables, sep=' ')
    for clause in clauses:
        print(' '.join(map(str, clause)), end=' 0\n')


def hamiltonian_path_to_sat(vertices, edges):
    # Each vertex belongs to a path.
    clauses = [[varnum(i, j, vertices) for j in range(1, vertices + 1)] for i in range(1, vertices + 1)]

    # No vertex appears twice in the path
    for i in range(1, vertices + 1):
        for j, k in itertools.combinations(range(1, vertices + 1), 2):
            clauses.append([-varnum(i, j, vertices), -varnum(i, k, vertices)])

    # Each position in a path is occupied by some vertex.
    for i in range(1, vertices + 1):
        clauses.append([varnum(i, i, vertices) for _ in range(1, vertices + 1)])

    # No two vertices j and k occupy the same position in the path.
    for i in range(1, vertices + 1):
        for j, k in itertools.combinations(range(1, vertices + 1), 2):
            clauses.append([-varnum(j, i, vertices), -varnum(k, i, vertices)])

    # Nonadjacent nodes j and k cannot be adjacent in the path.
    for i in range(1, vertices):
        for j, k in itertools.product(range(1, vertices + 1), repeat=2):
            if j != k and (j, k) not in edges:
                clauses.append([-varnum(j, i, vertices), -varnum(k, i + 1, vertices)])

    return clauses


if __name__ == '__main__':
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    print_equisatisfiable_sat_formula(n, set(edges))
