#! /usr/bin/python3

import sys, os, time
from typing import Tuple


def part1(steps: int) -> int:
    spinLock = [ 0 ]
    position = 0
    for number in range(1, 2017 + 1):
        position = (position + steps) % len(spinLock) + 1
        spinLock.insert(position, number)
    return spinLock[position + 1]


def part2(steps: int) -> int:
    position = 0
    result = 0
    for number in range(1, 5 * 10 ** 7 + 1):
        position = ((position + steps) % number) + 1
        if (position == 1):
            result = number
    return result


def solve(steps: int) -> Tuple[int,int]:
    return (
        part1(steps),
        part2(steps)
    )

def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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