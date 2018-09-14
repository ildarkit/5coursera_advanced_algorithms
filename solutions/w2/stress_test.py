from gaussian_elimination import gaussian_elimination
import numpy as np
from random import randint

MAX_ERR = 1e-2
EPS = 1e-2


def abs_error(x, y):
    return abs(x - y)


def rel_error(x, y):
    return abs(x - y) / abs(x)


def test_generator(num_tests, n_min=0, n_max=20, ai_min=-1000, ai_max=1000):
    """
    @brief      Generates random test values for a and b given a set of constraints.
                Assumes only integer values for each ai, and that there exists a unique solution.
                Default constraint parameters are set to the constraints listed in the instructions.
                This is a generator, so it "yields" instead of "returns".

    @param      num_tests  The number tests
    @param      n_min      The n minimum
    @param      n_max      The n maximum
    @param      ai_min     The ai minimum
    @param      ai_max     The ai maximum

    @return     On each iteration, it yields a tuple (i, a, b) where i is the number of the test,
                a and b are the test values.
    """
    for i in range(num_tests):
        n = randint(n_min, n_max)
        a = [[randint(ai_min, ai_max) for _ in range(n)] for _ in range(n)]
        if n != 0:  # If n is 0 then we have empty matrices, no need for computing determinant
            # If determinant of matrix A is 0 (or in other words, less than EPS)
            # then there is no unique solution since at least one row is a linear combination
            # of the others
            while abs(np.linalg.det(a)) < EPS:
                a = [[randint(ai_min, ai_max) for _ in range(n)] for _ in range(n)]
        b = [randint(ai_min, ai_max) for _ in range(n)]  # Assuming each E takes the same constraints as ai
        yield (i, a, b)


def are_equal(result, answer):
    # Test if your solution and correct
    # answer are the same
    for x, y in zip(answer, result):
        if abs_error(x, y) > MAX_ERR:
            return False
        if rel_error(x, y) > MAX_ERR:
            return False
    return True


def print_matrix(m):
    # Prints 2d array by row instead of comma-seperated
    for row in m:
        print(row)


def main():
    num_tests = 50  # Number of tests to generate
    num_correct = 0
    for i, a, b in test_generator(num_tests):
        # a and b get mutated in the implementation when
        # performing reduction, so lets keep copies
        # of the originals
        a_original = []
        b_original = []
        test = []
        for i, row in enumerate(a):
            a_original.append([])
            test.append([])
            for e in row:
                a_original[-1].append(e)
                test[-1].append(e)
            test[-1].append(b[i])
            b_original.append(b[i])

        ## Get the result from your implementation
        result = gaussian_elimination(
            test)  # NOTE: This was SolveEquation(equation) in the template file, so change this line if necessary

        ## Get the true solution from numpy
        # If either a and b are empty, then just set
        # the answer to an empty list to avoid
        # raising an error from numpy
        if a and b:
            answer = list(np.linalg.solve(a, b))
        else:
            answer = []

        ## Test their equality
        if are_equal(result, answer):
            # print("Pass!")
            num_correct += 1
        else:
            print("FAIL!")
            print("Test #%d:" % (i + 1))
            print("a:")
            print_matrix(a_original)
            print("b: %r" % b_original)
            print("Your result: %r" % result)
            print("Correct answer: %r" % answer)
    # Compute passing rate and print
    pass_rate = (num_correct / num_tests) * 100
    print("Overall pass rate was %.2f%%" % pass_rate)


if __name__ == '__main__':
    main()