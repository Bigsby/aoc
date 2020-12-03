#! /usr/bin/python3

import sys
from typing import Tuple, List
from functools import reduce

from common import getInput, getNextPosition, calculateTrees

def main():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    grid = getInput(sys.argv[1])
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
