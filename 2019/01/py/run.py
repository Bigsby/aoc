#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def getFuel(mass: int) -> int:
    total = 0
    currentMass = mass
    while True:
        fuel = currentMass // 3 - 2
        if fuel <= 0:
            break
        total += fuel
        currentMass = fuel
    return total


def part2(masses: List[int]) -> int:
    return sum(getFuel(mass) for mass in masses)


def solve(masses: List[int]) -> Tuple[int,int]:
    return (
        sum((mass // 3) - 2 for mass in masses),
        sum(getFuel(mass) for mass in masses)
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