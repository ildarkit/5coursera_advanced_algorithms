from itertools import chain
from random import randrange, choice

VARS = 3
MIN_VARIABLES = -VARS
MAX_VARIABLES = VARS + 1


def append_var(clauses, v):
    if len(clauses[-1]) < 2:
        clauses[-1].append(v)
    else:
        clauses.append([v])


def two_cnf_generator():
    variables = {i: j for i, j in enumerate(chain(range(MIN_VARIABLES, 0), range(1, MAX_VARIABLES))) if j}
    len_variables = len(variables) // 2
    nclauses = randrange(round(len_variables / 2), len_variables*(len_variables - 1))
    clauses = [[len_variables, nclauses]]
    while len(clauses) - 1 < nclauses or (len(clauses) - 1 == nclauses and len(clauses[-1]) < 2):
        if variables:
            index = choice(list(variables.keys()))
            v = variables.pop(index)
        else:
            v = choice((randrange(MIN_VARIABLES, 0), randrange(1, MAX_VARIABLES)))
        append_var(clauses, v)

    return clauses


if __name__ == '__main__':
    print(two_cnf_generator())






