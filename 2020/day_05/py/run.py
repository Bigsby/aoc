#! /usr/bin/python3

import sys, os, time
from typing import List


def part1(puzzleInput: List[int]) -> int:
    return max(puzzleInput)


def part2(puzzleInput: List[int]) -> int:
    ids = sorted(puzzleInput)
    print(ids)
    lastId = ids[0]
    for currentId in ids:
        if currentId - lastId == 2:
            return lastId + 1
        lastId = currentId
    raise Exception("Not found")


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0"), 2) for line in file.readlines() ]


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