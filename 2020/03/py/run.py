#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from functools import reduce

Trees = List[complex]


def calculateTrees(trees: Trees, step: complex) -> int:
    yLimit = max(p.imag for p in trees) + 1
    xLimit = max(p.real for p in trees) + 1
    currentPosition = 0j
    treeCount = 0
    while currentPosition.imag < yLimit:
        treeCount += (currentPosition.real % xLimit) + currentPosition.imag * 1j in trees
        currentPosition += step
    return treeCount


STEPS = [
    1 + 1j,
    3 + 1j,
    5 + 1j,
    7 + 1j,
    1 + 2j
]
def solve(trees: Trees) -> Tuple[int,int]:
    return (
        calculateTrees(trees, 3 + 1j),
        reduce(lambda current, step: current * calculateTrees(trees, step), STEPS, 1)
    )


def getInput(filePath: str) -> Trees:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        trees = []
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line):
                if c == '#':
                    trees.append(x + y * 1j)
    return trees 


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()