#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple


PATTERN = [0, 1, 0, -1]


def getValue(offset: int, signal: List[int]) -> int:
    total = 0
    for index, number in enumerate(signal):
        indexInPattern = ((index + 1) // offset) % len(PATTERN)
        multiplier = PATTERN[indexInPattern]
        total += number * multiplier
    return abs(total) % 10


def nextPhase(signal: List[int]) -> List[int]:
    result: List[int] = []
    for index in range(len(signal)):
        result.append(getValue(index + 1, signal))
    return result


def part1(signal: List[int]) -> str:
    signal = list(signal)
    for _ in range(100):
        signal = nextPhase(signal)
    return "".join([str(n) for n in signal[:8]])


def part2(signal: List[int]) -> str:
    offset = int("".join(map(str, signal[:7])))
    signal = (signal*10000)[offset:]
    for _ in range(100):
        sum = 0
        for i in range(len(signal)-1, -1, -1):
            signal[i] = sum = (sum + signal[i]) % 10
    return "".join(map(str, signal[:8]))


def solve(signal: List[int]) -> Tuple[str, str]:
    return (
        part1(signal),
        part2(signal)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        return [int(c) for c in file.read().strip()]


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
