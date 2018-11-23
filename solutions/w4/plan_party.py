# uses python3

import sys
import threading


INF = 100000000


class Vertex:
    """
    Vertex with its weight, independent subset weight and list of children.
    """
    def __init__(self, weight):
        self.weight = weight
        self.independent_weight = INF
        self.children = []


def read_tree():
    """
    Input the tree.
    :return: tree
    """
    size = int(input())
    tree = [Vertex(w) for w in map(int, input().split())]
    for i in range(1, size):
        a, b = list(map(int, input().split()))
        tree[a - 1].children.append(b - 1)
        tree[b - 1].children.append(a - 1)
    return tree


def dfs(tree, vertex, parent):
    """
    Traversing the tree in depth.
    :param tree: tree
    :param vertex: current vertex
    :param parent: parent of the current vertex
    :return: maximum possible weight of independent subsets
    """
    if tree[vertex].independent_weight == INF:

        independent_children_weight = 0
        independent_self_grandchildren_weight = tree[vertex].weight
        for child in tree[vertex].children:
            if child != parent:
                for grandchild in tree[child].children:
                    if grandchild != vertex:
                        independent_self_grandchildren_weight += dfs(tree, grandchild, child)

                independent_children_weight += dfs(tree, child, vertex)

        tree[vertex].independent_weight = max(independent_self_grandchildren_weight,
                                              independent_children_weight)

    return tree[vertex].independent_weight


def max_weight_independent_tree_subset(tree):
    size = len(tree)
    if not size:
        return size
    return dfs(tree, 0, -1)


def main():
    # function is executed in thread
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
