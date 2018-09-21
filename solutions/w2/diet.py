# python3
from sys import stdin


class Tableau:
    def __init__(self, source, b, pleasures):
        self.source = source
        self.simplex_table = []
        self.b = b
        self.pleasures = pleasures
        self.basis_values = []

    def pivot_column(self):
        pass

    def pivot_row(self, row):
        pass

    def pivot(self, row, column):
        pass

    def swap(self):
        pass

    def check(self):
        pass


def solve_diet_problem(n, m, a, b, c):
    # Write your code here
    simplex = Tableau(a, b, c)
    while not simplex.check():
        pivot_column = simplex.pivot_column()
        pivot_row = simplex.pivot_row(pivot_column)
        simplex.pivot(pivot_row, pivot_column)
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
