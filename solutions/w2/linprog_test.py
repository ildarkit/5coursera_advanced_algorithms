import numpy as np
from scipy.optimize import linprog


if __name__ == '__main__':
    # A = np.array([[-1, 0], [1, 0], [0, -1], [0, 1]])
    # b = np.array([-59, 78, -34, 87])
    # c = np.array([100, -5])
    A = np.array([[-90, -98, -30], [-70, -85, 11]])
    b = np.array([14313, -18638])
    c = np.array([-90, -42, 46])
    linprog_res = linprog(-c, A_ub=A, b_ub=b, options={'tol': 1e-3})
    result = 'Unknown'
    if linprog_res.status == 3:
        result = 'Infinity'
    elif linprog_res.status == 2:
        result = 'No solution'
    else:
        result = 'Bounded solution'
        solution_x = linprog_res.x
        print('x_ref =', ' '.join(list(map(lambda x: '%.18f' % float(x), solution_x))))
    print(result)