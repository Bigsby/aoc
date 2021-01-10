#! /usr/bin/python3

import sys, os, time
from typing import List
import re
from itertools import permutations


def part1(lines: List[List[int]]) -> int:
    total = 0
    for line in lines:
        maximum = max(line)
        minimum = min(line)
        total += maximum - minimum

    return total


def part2(lines: List[List[int]]) -> int:
    total = 0
    for line in lines:
        pairs = permutations(line, 2)
        for pair in pairs:
            if pair[0] > pair[1] and pair[0] % pair[1] == 0:
                total += pair[0] // pair[1]

    return total


lineRegex = re.compile(r"\d+")
def getInput(filePath: str) -> List[List[int]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ [ int(i) for i in lineRegex.findall(line) ] for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()