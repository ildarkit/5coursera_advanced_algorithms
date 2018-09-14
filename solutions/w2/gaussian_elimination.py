# python3
EPS = 1e-2
PRECISION = '.6f'


def gaussian_elimination(a):
    h = k = 0
    m = len(a)
    n = len(a[0])
    while h < m and k < n - 1:
        pivot = abs(a[h][k])
        pivot_row = h
        for i in range(h + 1, m):
            diff = abs(a[i][k]) - pivot
            if diff > EPS:
                pivot = abs(a[i][k])
                pivot_row = i
        if abs(a[pivot_row][k] - EPS) < EPS:  # a[pivot_row][k] == 0
            k += 1
        else:
            # swap
            a[h], a[pivot_row] = a[pivot_row], a[h]
            if abs(a[h][k]) > EPS:  # abs(a[h][k]) > 0
                # rescale
                scale = a[h][k]
                for j in range(n):
                    if abs(a[h][j]) > 0.0 + EPS:  # a[h][j] != 0
                        a[h][j] /= scale
            for i in range(m):
                subtract = False
                if i != h:
                    f = abs(a[i][k] / a[h][k])
                    if f < EPS:
                        continue
                    # (a[i][k] > 0 and a[h][k] > 0) or (a[i][k] < 0 and a[h][k] < 0)
                    if (a[i][k] > EPS and a[h][k] > EPS) or (a[i][k] < -EPS and a[h][k] < -EPS):
                        subtract = True
                else:
                    continue
                a[i][k] = 0.0
                for j in range(k + 1, n):
                    if subtract:
                        a[i][j] -= a[h][j]*f
                    else:
                        a[i][j] += a[h][j]*f
            h += 1
            k += 1
    # return ' '.join([format(row[-1], PRECISION) for row in a])
    return [row[-1] for row in a]


def read_equation():
    size = int(input())
    a = []
    for row in range(size):
        line = list(map(float, input().split()))
        a.append(line)
    return a


if __name__ == "__main__":
    matrix = read_equation()
    print(gaussian_elimination(matrix))
