# python3
from sys import stdin


def solve_diet_problem(n, m, A, b, c):
    # Write your code here
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
