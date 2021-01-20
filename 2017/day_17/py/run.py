#! /usr/bin/python3

import sys, os, time
from collections import deque
from typing import Deque


def runSpinLock(steps: int, iterations: int) -> Deque[int]:
    spinLock = deque([0])
    for number in range(1, iterations + 1):
        spinLock.rotate(-steps)
        spinLock.append(number)
    return spinLock


def part1(steps: int) -> int:
    return runSpinLock(steps, 2017)[0]


def part2(steps: int) -> int:
    spinLock = runSpinLock(steps, 5 * 10 ** 7 + 1)
    return spinLock[spinLock.index(0) + 1]


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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