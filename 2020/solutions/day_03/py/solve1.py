#! /usr/bin/python3

import sys
from common import getInput, getNextPosition, calculateTrees

def main():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    grid = getInput(sys.argv[1])
    treeCount = calculateTrees(grid, (1, 3))

    print("Trees found:", treeCount)

if __name__ == "__main__":
    main()
