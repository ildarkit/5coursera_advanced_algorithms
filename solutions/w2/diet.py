# python3
from sys import stdin


INF = float('INF')


class Tableau:
    def __init__(self, m, source, b, pleasures):
        self.source = source
        self.simplex_table = []
        self.b = b
        self.pleasures = pleasures
        self.basis_values = [0 for _ in range(m)]

    def init_simplex_table(self):
        for i, bi in enumerate(self.b):
            self.simplex_table.append([bi])
            self.simplex_table[-1].extend(self.source[i])
            self.basis_values.append(bi)
        func = [0]
        for ci in self.pleasures:
            func.append(ci * -1)
        self.simplex_table.append(func)

    def pivot_column(self):
        pivot_col = -1
        min_negative = INF
        for j in range(1, len(self.simplex_table[-1])):
            if self.simplex_table[-1][j] < 0 and abs(self.simplex_table[-1][j]) < min_negative:
                min_negative = abs(self.simplex_table[-1][j])
                pivot_col = j
        return pivot_col

    def pivot_row(self, pivotcol):
        min_ratio = INF
        pivotrow = -1
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

        self.simplex_table = new_simplex_table

    def swap(self):
        pass

    def is_optimum(self):
        result = True
        for j in range(1, self.simplex_table[-1]):
            if self.simplex_table[-1][j] < 0:
                result = False
                break
        return result


def solve_diet_problem(n, m, a, b, c):
    # Write your code here
    simplex_method = Tableau(m, a, b, c)
    simplex_method.init_simplex_table()
    while not simplex_method.is_optimum():
        pivotcol = simplex_method.pivot_column()
        pivotrow = simplex_method.pivot_row(pivotcol)
        simplex_method.transform(pivotrow, pivotcol)
    return [0, [0] * m]


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
    if anst == 0:
        print("Bounded solution")
        print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
    if anst == 1:
        print("Infinity")
