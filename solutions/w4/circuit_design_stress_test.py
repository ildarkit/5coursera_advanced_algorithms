from circuit_design import is_satisfiable, DEBUG
from two_cnf import two_cnf_generator


ERROR_THRESHOLD = 0.1


def is_satisfy(var1, var2, var_map):
    return is_true(var1, var_map) or is_true(var2, var_map)


def is_true(var, var_map):
    v = var_map.get(var, vars_map[-var])
    if var < 0:
        v = not v
    return v


if __name__ == '__main__':
    stop = 1000
    total = 0
    err = 0
    DEBUG = True
    while True:
        total += 1
        clauses = two_cnf_generator()
        try:
            result = is_satisfiable(clauses[0][0], clauses)
        except (TypeError, IndexError) as e:
            print('(ERROR):', e)
            print('clauses={}'.format(clauses))
            continue
        if result:
            vars_map = {-i-1 if result[i] else i+1: result[i] for i in range(clauses[0][0])}
            is_correct = True
            for var1, var2 in result[1:]:
                if not is_satisfy(var1, var2, vars_map):
                    is_correct = False
                    break
            if not is_correct:
                err += 1
                print('INCORRECT ANSWER FOR:')
                print(clauses)
        else:
            print('(DEBUG) Need check for clauses:')
            print(clauses)
        if total * ERROR_THRESHOLD <= err and err > 0 or total >= stop:
            break
        if total % 100 == 0:
            print('total = {}, err = {}'.format(total, err))