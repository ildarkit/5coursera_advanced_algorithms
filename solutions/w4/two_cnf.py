from itertools import chain
from random import randint, randrange, choice

VARS = 100  # max number of variables


def append_var(clauses, v):
    if len(clauses[-1]) < 2:
        clauses[-1].append(v)
    else:
        clauses.append([v])


def shake(seq):
    """
    Makes the sequence unordered.
    :param seq: list of variables
    """
    indexes = range(len(seq))
    for _ in range(len(seq)):
        first = choice(indexes)
        second = choice(indexes)
        seq[first], seq[second] = seq[second], seq[first]


def two_cnf_generator():
    """
    The clauses generator in 2-cnf formula.
    First list contain number of values and number of clauses.
    "-" means negating the variable.
    For example, a line “2 3” represents a clause (x2 OR x3),
    line “1 -4” represents (x1 OR NOT x4).
    :return: List of clauses lists.
    """
    n = randint(1, VARS)
    min_variables = -n
    max_variables = n + 1
    # list of variables
    variables = [i for i in chain(range(min_variables, 0), range(1, max_variables)) if i]
    shake(variables)
    len_variables = len(variables)
    if len_variables / 2 % 1 > 0.0:
        low = round(len_variables / 2) + 1
    else:
        low = len_variables // 2
    if len_variables // 2 > 3:
        nclauses = randrange(low, (len_variables // 2)*(len_variables // 2 - 1))
    else:
        nclauses = low
    clauses = [[len(variables) // 2, nclauses]]
    while len(clauses) - 1 < nclauses or (len(clauses) - 1 == nclauses and len(clauses[-1]) < 2):
        if variables:
            v = variables.pop()
        else:
            v = choice((randrange(min_variables, 0), randrange(1, max_variables)))
        append_var(clauses, v)

    return clauses


if __name__ == '__main__':
    for line in two_cnf_generator():
        print('{:d} {:d}'.format(line[0], line[1]))





