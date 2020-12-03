#! /usr/bin/python3

from functools import reduce

from common import getInput, getNextPosition, calculateTrees


def main():
    grid = getInput()
    steps = [
        (1, 1),
        (1, 3),
        (1, 5),
        (1, 7),
        (2, 1)
       ]
    treeCount = reduce(lambda current, step: current * calculateTrees(grid, step), steps, 1)
    print("Trees found:", treeCount)


if __name__ == "__main__":
    main()
