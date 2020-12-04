#! /usr/bin/python3

from common import getInput, getNextPosition, calculateTrees


def main():
    grid = getInput()
    treeCount = calculateTrees(grid, (1, 3))

    print("Trees found:", treeCount)


if __name__ == "__main__":
    main()
