#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def part2(seats: List[int]) -> int:
    lastId = min(seats)
    for currentId in sorted(seats):
        if currentId - lastId == 2:
            return lastId + 1
        lastId = currentId
    raise Exception("Seat not found")


def solve(seats: List[int]) -> Tuple[int,int]:
    return (
        max(seats),
        part2(seats)
    )

def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line.replace("B", "1").replace("F", "0").replace("R", "1").replace("L", "0"), 2) for line in file.readlines() ]


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