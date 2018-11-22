# uses python3

import sys
import threading


class Vertex:
    def __init__(self, weight):
        self.weight = weight
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
    for child in tree[vertex].children:
        if child != parent:
            dfs(tree, child, vertex)
    # This is a template function for processing a tree using depth-first search.
    # Write your code here.
    # You may need to add more parameters to this function for child processing.


def max_weight_independent_tree_subset(tree):
    size = len(tree)
    if size == 0:
        return 0
    dfs(tree, 0, -1)
    # You must decide what to return.
    return 0


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
