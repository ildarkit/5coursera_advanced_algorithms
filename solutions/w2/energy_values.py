# python3

EPS = 1e-6
PRECISION = 20


class Equation:
    def __init__(self, a, b):
        self.a = a
        self.b = b


class Position:
    def __init__(self, column, row):
        self.column = column
        self.row = row


def read_equation():
    size = int(input())
    a = []
    b = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line[:size])
        b.append(line[size])
    return Equation(a, b)


def select_pivot_element(a, used_rows, used_columns):
    # This algorithm selects the first free element.
    # You'll need to improve it to pass the problem.
    pivot_element = Position(0, 0)
    while used_rows[pivot_element.row]:
        pivot_element.row += 1
    while used_columns[pivot_element.column]:
        pivot_element.column += 1
    return pivot_element


def swap_lines(a, b, used_rows, pivot_element):
    a[pivot_element.column], a[pivot_element.row] = a[pivot_element.row], a[pivot_element.column]
    b[pivot_element.column], b[pivot_element.row] = b[pivot_element.row], b[pivot_element.column]
    used_rows[pivot_element.column], used_rows[pivot_element.row] = used_rows[pivot_element.row], used_rows[pivot_element.column]
    pivot_element.row = pivot_element.column


def process_pivot_element(a, b, pivot_element):
    # Write your code here
    pass


def mark_pivot_element_used(pivot_element, used_rows, used_columns):
    used_rows[pivot_element.row] = True
    used_columns[pivot_element.column] = True


def solve_equation(equation):
    a = equation.a
    b = equation.b
    size = len(a)

    used_columns = [False] * size
    used_rows = [False] * size
    for step in range(size):
        pivot_element = select_pivot_element(a, used_rows, used_columns)
        swap_lines(a, b, used_rows, pivot_element)
        process_pivot_element(a, b, pivot_element)
        mark_pivot_element_used(pivot_element, used_rows, used_columns)

    return b


def print_column(column):
    size = len(column)
    for row in range(size):
        print("%.20lf" % column[row])


if __name__ == "__main__":
    equation = read_equation()
    solution = solve_equation(equation)
    print_column(solution)
    exit(0)
