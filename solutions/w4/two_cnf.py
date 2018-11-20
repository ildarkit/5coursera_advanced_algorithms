from itertools import chain
from random import randint, randrange, choice

VARS = 3  # max number of variables


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


def number_pair_combinations(n):
    pair_comb = 0
    for i in range(1, n + 1):
        pair_comb += n - i
    return pair_comb


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
    nclauses = randrange(low, number_pair_combinations(len_variables) + 1)
    clauses = [[len(variables) // 2, nclauses]]
    unique_clauses = dict()
    i = 0
    while i < nclauses*2:
        if variables:
            v = variables.pop()
        else:
            v = choice((randrange(min_variables, 0), randrange(1, max_variables)))
        append_var(clauses, v)
        i += 1
        if len(clauses[-1]) == 2:
            v1, v2 = clauses[-1]
            if not unique_clauses.get((v1, v2)):
                unique_clauses[(v1, v2)] = 1
                unique_clauses[(v2, v1)] = 1
            else:
                i -= 2
                # remove the clause, because there is already such
                clauses.pop()

    return clauses


if __name__ == '__main__':
    for line in two_cnf_generator():
        print('{:d} {:d}'.format(line[0], line[1]))





