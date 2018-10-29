# python3
import itertools


def varnum(i, j, lenght):
    """
    Calculating the variable x_ij for the vertex j on position i.
    :param i: index in Hamiltonian graph
    :param j: vertex
    :return: boolean variable corresponding to the vertex j.
    """
    return (i - 1)*lenght + j


def print_equisatisfiable_sat_formula(vertices, clauses):
    """
    This solution prints a satisfiable formula.
    """
    variables = vertices * vertices
    print(len(clauses), variables, sep=' ')
    for clause in clauses:
        print(' '.join(map(str, clause)), end=' 0\n')


def hamiltonian_path_to_sat(vertices, edges):
    vertices_range = range(1, vertices + 1)
    # №1. Each vertex "j" belongs to a path.
    clauses = [
        [varnum(i, j, vertices) for i in vertices_range] for j in vertices_range
    ]

    # №2. No vertex appears twice in the path
    for j, k in itertools.combinations(vertices_range, 2):
        for i in vertices_range:
            clauses.append([-varnum(i, j, vertices), -varnum(i, k, vertices)])

    # №3. Each position "i" in a path is occupied by some vertex "j".
    for i in vertices_range:
        clauses.append([varnum(i, j, vertices) for j in vertices_range])

    # №4. No two vertices "j" and "k" occupy the same position "i" in the path.
    for j, k in itertools.combinations(vertices_range, 2):
        for i in vertices_range:
            clauses.append([-varnum(i, j, vertices), -varnum(i, k, vertices)])

    # №5. Non-adjacent nodes "j" and "k" cannot be adjacent in the path.
    for j, k in itertools.product(vertices_range, repeat=2):
        if j != k and (j, k) not in edges:
            for i in range(1, vertices):
                clauses.append([-varnum(i, j, vertices), -varnum(i + 1, k, vertices)])

    return clauses


if __name__ == '__main__':
    n, m = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(m)]
    clauses = hamiltonian_path_to_sat(n, set(edges))
    print_equisatisfiable_sat_formula(n, clauses)