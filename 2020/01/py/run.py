#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from itertools import combinations
from functools import reduce


def getCombination(numbers: List[int], length: int) -> int:
    for combination in combinations(numbers, length):
        if sum(combination) == 2020:
            return reduce(lambda soFar, number: soFar * number, combination)
    raise Exception("Numbers not found")


def solve(numbers: List[int]) -> Tuple[int,int]:
    return (
        getCombination(numbers, 2),
        getCombination(numbers, 3)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line) for line in file.readlines() ]


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