# python3
from sys import stdin


INF = float('INF')
INF_CONSTRAINT = 10**9
EPS = 1e-15  # floating-point error
ZERO = -1e-6
PRECISION = 11
NO_SOLUTION = 1
BOUNDED_SOLUTION = 2
INF_SOLUTION = -1


class Simplex:
    """
    Simplex method for solving LP problem.
    The essence of the simplex method is to purposefully search for feasible solutions,
    in which the objective function “improves”, or at least “does not deteriorate”
    at each subsequent step of the solution (iteration).
    """
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

    def init_simplex_table(self):
        len_basis = len(self.basis_indexes)
        for i, bi in enumerate(self.b):
            self.simplex_table.append([bi])
            self.simplex_table[-1].extend(self.source[i])
            self.basis_values.append(bi)
            self.basis_indexes.append(i + len_basis)
        # To distinguish between bounded and unbounded cases,
        # we add another inequality to the original problem.
        self.basis_values.append(INF_CONSTRAINT)
        self.basis_indexes.append(len(self.basis_indexes))
        self.simplex_table.append([INF_CONSTRAINT])
        func = [0]
        for ci in self.pleasures:
            func.append(ci * -1)
            self.simplex_table[-1].append(1)
        self.simplex_table.append(func)

    def pivot_column(self, solution_is_valid):
        """
        Search of pivot column.
        :param solution_is_valid: Sign of admissibility of the basis solution.
        :return: index of pivot column
        """
        if solution_is_valid:
            # If the basis solution is valid, then any such column (except for the free numbers column)
            # is taken as pivot column, in the row of the objective function of which
            # there is an element that does not correspond to the sign of the optimality sign.
            min_negative = INF
            for j in range(1, len(self.simplex_table[-1])):
                if self.simplex_table[-1][j] + EPS < EPS and self.simplex_table[-1][j] + EPS < min_negative:
                    min_negative = self.simplex_table[-1][j]
                    pivot_col = j
        else:
            # If the basis solution is not valid, then a negative element is selected
            # in the line containing a negative free number. The column in which the selected item
            # is located is accepted as pivot column.
            pivot_col = -1
            for i in range(len(self.simplex_table) - 1):
                if self.simplex_table[i][0] + EPS < EPS:
                    for j in range(1, len(self.simplex_table[i])):
                        if self.simplex_table[i][j] + EPS < EPS:
                            pivot_col = j
                            break
                if pivot_col != -1:
                    break
        return pivot_col

    def pivot_row(self, pivotcol):
        """
        Search of pivot row.
        Positive estimated ratios of free numbers to the elements of the pivot column
        are calculated (for the row of the objective function, the estimated ratio is not calculated).
        :param pivotcol: index of pivot column
        :return: index of pivot row
        """
        min_ratio = INF
        pivotrow = 0
        for i in range(len(self.simplex_table) - 1):
            if self.simplex_table[i][pivotcol] + EPS < 0.0 or self.simplex_table[i][pivotcol] > EPS:
                # self.simplex_table[i][pivotcol] != 0.0
                ratio = self.simplex_table[i][0] / self.simplex_table[i][pivotcol]
                if ratio > EPS and ratio + EPS < min_ratio:
                    min_ratio = ratio
                    pivotrow = i
        return pivotrow

    def transform(self, pivotrow, pivotcol):
        """
        Transform simplex table.
        :param pivotrow: index of pivot row
        :param pivotcol: index of pivot column
        """
        new_simplex_table = []
        pivot = self.simplex_table[pivotrow][pivotcol]

        for i in range(len(self.simplex_table)):
            new_simplex_table.append([])
            for j in range(len(self.simplex_table[0])):
                if i != pivotrow and j != pivotcol:
                    # Elements located in cells whose indices are not equal to the pivot row and column,
                    # the new simplex table is calculated according to the "rectangle" rule.
                    #
                    # "Rectangle" rule.
                    # Mentally, in the source simplex table we draw a rectangle,
                    # one vertex of which coincides with the pivot element,
                    # and the other with the element whose value we are counting.
                    # The remaining two vertices are determined uniquely.
                    # Then the desired element of the new simplex table will be equal
                    # to the corresponding element of the original simplex table minus the fraction,
                    # the denominator of which is the pivot element of the original simplex table,
                    # and the numerator is the product of the elements from two unused vertices
                    # of the rectangle in the original simplex table.
                    ratio = self.simplex_table[pivotrow][j]*self.simplex_table[i][pivotcol] / pivot
                    new_element = self.simplex_table[i][j] - ratio
                elif i == pivotrow and j == pivotcol:
                    # In the new simplex table, in the cell where the pivot element
                    # of the original simplex table was, write the value inverse to it.
                    new_element = 1 / pivot
                elif i == pivotrow:
                    # The elements located in the cells of the pivot row of the original
                    # simplex table are divided into the pivot element and recorded in the similar
                    # (corresponding) cells of the new simplex table.
                    new_element = self.simplex_table[i][j] / pivot
                else:
                    # The elements located in the cells of the pivot column of the original
                    # simplex table are divided into the pivot element,
                    # the result is taken with the opposite sign
                    new_element = - self.simplex_table[i][j] / pivot
                new_element = round(new_element, PRECISION)
                new_simplex_table[-1].append(new_element)
                if j == 0 and i < len(self.simplex_table) - 1:
                    # Write the new value of the basis variable.
                    basis_value_index = self.basis_indexes[i + len(self.simplex_table[0]) - 1]
                    self.basis_values[basis_value_index] = new_element

        self.simplex_table = new_simplex_table

    def swap(self, free, basis):
        """
        Swapping of free and basis variables.
        Variables corresponding to the pivot row and the pivot column are swapped in the new simplex table.
        In this case, the basis variable becomes free and vice versa.
        :param free: index of free variable
        :param basis: index of basis variable
        """
        self.basis_indexes[free], self.basis_indexes[basis] = self.basis_indexes[basis], self.basis_indexes[free]
        free_index = self.basis_indexes[free]
        basis_index = self.basis_indexes[basis]
        self.basis_values[free_index], self.basis_values[basis_index] = (self.basis_values[basis_index],
                                                                         self.basis_values[free_index])

    def no_solution(self):
        """
        Check for compatibility of the constraint system
        of the linear programming problem (feature 1).
        Restrictions are incompatible if there is not a single negative element
        in any line (except the line of the objective function) having a negative free number.
        :return: 1, if no solution, else 0
        """
        result = 0
        for i in range(len(self.simplex_table) - 1):
            if self.simplex_table[i][0] + EPS < ZERO:
                result = NO_SOLUTION
                for j in range(1, len(self.simplex_table[i])):
                    if self.simplex_table[i][j] + EPS < EPS:
                        result = 0
                        break
                if result == NO_SOLUTION:
                    break
        return result

    def is_bounded(self):
        """
        Checking the boundedness of the objective function (feature 2).
        The objective function is bounded in the area of feasible solutions,
        i.e. there is a finite maximum (minimum) value of the objective function
        if at each iteration in each column, in the row of the objective function
        of which there is a negative (positive) element, there is at least one positive element
        (this characteristic does not apply to the column of free numbers).
        :return: 2, if solution is bounded, else -1
        """
        result = BOUNDED_SOLUTION
        for j in range(1, len(self.simplex_table[-1])):
            if self.simplex_table[-1][j] + EPS < EPS:
                result = INF_SOLUTION
                for i in range(len(self.simplex_table) - 1):
                    if self.simplex_table[i][j] > EPS:  # self.simplex_table[i][j] > 0
                        result = BOUNDED_SOLUTION
                        break
        return result

    def is_valid(self):
        """
        Validation of the basis solution (feature 3).
        The basis solution is valid if all the free numbers
        in the simplex table (except the objective function line) are non-negative.
        :return:
        """
        result = True
        for b in self.basis_values:
            if b + EPS < ZERO:
                result = False
                break
        return result

    def is_optimum(self):
        """
        Checking the optimality of the solution (feature 4).
        The found valid basic solution will maximize (minimize) the objective function,
        i.e. will be optimal if all the elements (except for the element located
        in the column of free numbers) are positive (negative) in the row of the objective function.
        :return:
        """
        result = BOUNDED_SOLUTION
        for j in range(1, len(self.simplex_table[-1])):
            if self.simplex_table[-1][j] + EPS < ZERO:
                result = 0
                break

        return result


def solve_diet_problem(m, a, b, c):
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
        if result == INF_SOLUTION:
            # infinity
            break
        basis_solution_is_valid = simplex_method.is_valid()
        if basis_solution_is_valid:
            result = simplex_method.is_optimum()
            if result:
                # optimal solution
                break
        else:
            result = 0

        pivotcol = simplex_method.pivot_column(solution_is_valid=basis_solution_is_valid)
        pivotrow = simplex_method.pivot_row(pivotcol)
        simplex_method.transform(pivotrow, pivotcol)
        simplex_method.swap(pivotrow + m, pivotcol - 1)

    if result == BOUNDED_SOLUTION and round(sum(simplex_method.basis_values[:m])) + 2.0 >= INF_CONSTRAINT:
        result = INF_SOLUTION
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
    _, m, a, b, c = read_inputs()
    anst, ansx = solve_diet_problem(m, a, b, c)

    if anst == NO_SOLUTION:
        print("No solution")
    if anst == BOUNDED_SOLUTION:
        print("Bounded solution")
        print(' '.join(list(map(lambda x : '%.18f' % x, ansx))))
    if anst == INF_SOLUTION:
        print("Infinity")
