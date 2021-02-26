#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def part2(changes: List[int]) -> int:
    changesLength = len(changes)
    frequency = 0
    previous = set() 
    index = 0
    while frequency not in previous:
        previous.add(frequency)
        frequency += changes[index]
        index = (index + 1) % changesLength
    return frequency


def solve(changes: List[int]) -> Tuple[int,int]:
    return (
        sum(changes),
        part2(changes)
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