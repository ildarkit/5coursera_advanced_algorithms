# python3


def print_equisatisfiable_sat_formula():
    """
    This solution prints a simple satisfiable formula
    and passes about half of the tests.
    Change this function to solve the problem.
    """
    print("3 2")
    print("1 2 0")
    print("-1 -2 0")
    print("1 -2 0")

    
if __name__ == '__main__':
    n, m = map(int, input().split())
    edges = [list(map(int, input().split())) for _ in range(m)]
    print_equisatisfiable_sat_formula()
