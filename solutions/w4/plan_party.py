# uses python3

import sys
import threading


INF = 10000


class Vertex:
    def __init__(self, weight):
        self.weight = weight
        self.d = INF
        self.children = []


def read_tree():
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree


def dfs(tree, vertex, parent):
    if tree[vertex].d == INF:

        m1 = tree[vertex].weight
        m0 = 0
        for child in tree[vertex].children:
            if child != parent:
                for grandchild in tree[child].children:
                    if grandchild != vertex:
                        m1 += dfs(tree, grandchild, child)

                m0 += dfs(tree, child, vertex)

        tree[vertex].d = max(m1, m0)

    return tree[vertex].d


def max_weight_independent_tree_subset(tree):
    size = len(tree)
    if not size:
        return size
    return dfs(tree, 0, -1)


def main():
    tree = read_tree()
    weight = max_weight_independent_tree_subset(tree)
    print(weight)


if __name__ == '__main__':
    # This code is used to avoid stack overflow issues
    sys.setrecursionlimit(10 ** 6)  # max depth of recursion
    threading.stack_size(2 ** 26)  # new thread will get stack of such size
    t = threading.Thread(target=main)
    t.start()
    t.join()
