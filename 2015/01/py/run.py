#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def part2(directions: List[int]) -> int:
    currentFloor = 0
    for index, direction in enumerate(directions):
        currentFloor += direction
        if currentFloor == -1:
            return index + 1
    raise Exception("Did not go below 0!")


def solve(directions: List[int]) -> Tuple[int,int]:
    return (sum(directions), part2(directions))


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath) as file:
        return [ 1 if c == "(" else -1 for c in file.read().strip() ]


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