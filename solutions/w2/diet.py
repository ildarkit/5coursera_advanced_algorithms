# python3
from sys import stdin


INF = float('INF')
INF_CONSTRAINT = 10**9


class Simplex:
    def __init__(self, m, source, b, pleasures):
        self.source = source
        self.simplex_table = []
        self.b = b
        self.pleasures = pleasures
        self.basis_values = []
        self.basis_indexes = []
        for i in range(m):
            self.basis_values.append(0)
            self.basis_indexes.append(i)
        self.forced_pivot_col = 1

    def init_simplex_table(self):
        len_basis = len(self.basis_indexes)
        for i, bi in enumerate(self.b):
            self.simplex_table.append([bi])
            self.simplex_table[-1].extend(self.source[i])
            self.basis_values.append(bi)
            self.basis_indexes.append(i + len_basis)
        self.basis_values.append(INF_CONSTRAINT)
        self.basis_indexes.append(len(self.basis_indexes))
        self.simplex_table.append([INF_CONSTRAINT])
        func = [0]
        for ci in self.pleasures:
            func.append(ci * -1)
            self.simplex_table[-1].append(1)
        self.simplex_table.append(func)

    def pivot_column(self):
        pivot_col = self.forced_pivot_col
        min_negative = INF
        for j in range(self.forced_pivot_col, len(self.simplex_table[-1])):
            if self.simplex_table[-1][j] < 0 and self.simplex_table[-1][j] < min_negative:
                min_negative = self.simplex_table[-1][j]
                pivot_col = j
        return pivot_col

    def pivot_row(self, pivotcol):
        min_ratio = INF
        pivotrow = 0
        for i in range(len(self.simplex_table) - 1):
            if self.simplex_table[i][0] >= 0 and self.simplex_table[i][pivotcol] > 0:
                ratio = self.simplex_table[i][0] / self.simplex_table[i][pivotcol]
                if ratio < min_ratio:
                    min_ratio = ratio
                    pivotrow = i
        return pivotrow

    def transform(self, pivotrow, pivotcol):
        new_simplex_table = []
        pivot = self.simplex_table[pivotrow][pivotcol]
        if not pivot:
            self.forced_pivot_col = pivotcol + 1
            return False
        self.forced_pivot_col = 1
        for i in range(len(self.simplex_table)):
            new_simplex_table.append([])
            for j in range(len(self.simplex_table[0])):
                if i != pivotrow and j != pivotcol:
                    ratio = self.simplex_table[pivotrow][j]*self.simplex_table[i][pivotcol] / pivot
                    new_element = self.simplex_table[i][j] - ratio
                elif i == pivotrow and j == pivotcol:
                    new_element = 1 / pivot
                elif i == pivotrow:
                    new_element = self.simplex_table[i][j] / pivot
                else:
                    new_element = - self.simplex_table[i][j] / pivot
                new_simplex_table[-1].append(new_element)
                if j == 0 and i < len(self.simplex_table) - 1:
                    basis_value_index = self.basis_indexes[i + len(self.simplex_table[0]) - 1]
                    self.basis_values[basis_value_index] = new_element

        self.simplex_table = new_simplex_table
        return True

    def swap(self, free, basis):
        self.basis_indexes[free], self.basis_indexes[basis] = self.basis_indexes[basis], self.basis_indexes[free]
        free_index = self.basis_indexes[free]
        basis_index = self.basis_indexes[basis]
        self.basis_values[free_index], self.basis_values[basis_index] = (self.basis_values[basis_index],
                                                                         self.basis_values[free_index])

    def is_optimum(self):
        result = 2
        for j in range(1, len(self.simplex_table[-1])):
            if self.simplex_table[-1][j] < 0:
                result = 0
                break

        return result

    def no_solution(self):
        result = 0
        for i in range(len(self.simplex_table) - 1):
            if self.simplex_table[i][0] < 0:
                for j in range(1, len(self.simplex_table[i])):
                    if self.simplex_table[i][j] < 0:
                        return result
                result = -1
                break
        return result

    def is_bounded(self):
        result = 1
        neg = False
        for j in range(1, len(self.simplex_table[-1])):
            if self.simplex_table[-1][j] < 0:
                neg = True
                for i in range(len(self.simplex_table) - 1):
                    if self.simplex_table[i][j] > 0:
                        return 2
        if not neg:
            result = 2
        return result

    def is_valid(self):
        result = True
        for b in self.basis_values:
            if b < 0:
                result = False
                break
        return result


def solve_diet_problem(n, m, a, b, c):
    # Write your code here
    simplex_method = Simplex(m, a, b, c)
    simplex_method.init_simplex_table()
    result = 0
    while not result:
        result = simplex_method.no_solution()
        if result:
            # no solution
            break
        result = simplex_method.is_bounded()
        if result == 2:
            if simplex_method.is_valid():
                result = simplex_method.is_optimum()
                if result:
                    # optimal solution
                    break
        else:
            # infinity
            break
        pivotcol = simplex_method.pivot_column()
        pivotrow = simplex_method.pivot_row(pivotcol)
        if simplex_method.transform(pivotrow, pivotcol):
            simplex_method.swap(pivotrow + m, pivotcol - 1)
    if sum(simplex_method.basis_values[:m]) >= INF_CONSTRAINT:
        result = 1
    return [result, simplex_method.basis_values[:m]]


def read_inputs():
    n, m = list(map(int, stdin.readline().split()))
    a = []
    for i in range(n):
      a += [list(map(int, stdin.readline().split()))]
    b = list(map(int, stdin.readline().split()))
    c = list(map(int, stdin.readline().split()))
    return n, m, a, b, c


if __name__ == "__main__":
    n, m, a, b, c = read_inputs()
    anst, ansx = solve_diet_problem(n, m, a, b, c)

    if anst == -1:
        print("No solution")
    if anst == 2:
        print("Bounded solution")
        print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
    if anst == 1:
        print("Infinity")
