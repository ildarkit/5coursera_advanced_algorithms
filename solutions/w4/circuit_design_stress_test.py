import sys
import threading

import circuit_design
from two_cnf import two_cnf_generator


ERROR_THRESHOLD = 0.1


def is_satisfy(var1, var2, var_map):
    """
    Checking the clause in 2-cnf form for a given boolean variables.
    :param var1: first variable
    :param var2: second variable
    :param var_map: the values of these variables
    :return: True if clause is satisfy, else False
    """
    return is_true(var1, var_map) or is_true(var2, var_map)


def is_true(var, var_map):
    bool_value = var_map[abs(var)]
    if var < 0:
        bool_value = not bool_value
    return bool_value


def run_tests():
    stop = 1000
    total = 0
    err = 0
    circuit_design.DEBUG = True
    while True:
        total += 1
        clauses = two_cnf_generator()

        result = circuit_design.is_satisfiable(clauses[0][0], clauses[1:])

        if result:
            vars_map = {i + 1: result[i] for i in range(clauses[0][0])}
            is_correct = True
            for var1, var2 in clauses[1:]:
                if not is_satisfy(var1, var2, vars_map):
                    is_correct = False
                    break
            bool_assignment = " ".join(str(i if result[i - 1] else -i) for i in range(1, clauses[0][0] + 1))
            if not is_correct:
                err += 1
                print('(ERROR) INCORRECT ANSWER FOR:')
                print('clauses = {}'.format(clauses))
                print('boolean assignment is falsified = {}'.format(bool_assignment))
            else:
                print('(INFO) SATISFIABLE answer for clauses:')
                print(clauses)
                print('boolean assignment is satisfied = {}'.format(bool_assignment))
        elif circuit_design.DEBUG:
            print('(DEBUG) UNSATISFIABLE answer for clauses:')
            print(clauses)
        if total * ERROR_THRESHOLD <= err and err > 0 or total >= stop:
            break
        if total % 100 == 0:
            print('(INFO) total = {}, err = {}'.format(total, err))


if __name__ == '__main__':
    sys.setrecursionlimit(10 ** 6)  # max depth of recursion
    threading.stack_size(2 ** 26)  # new thread will get stack of such size
    t = threading.Thread(target=run_tests)
    t.start()
    t.join()
