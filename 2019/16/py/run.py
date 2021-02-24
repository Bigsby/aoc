#! /usr/bin/python3

import sys, os, time
from typing import List


PATTERN = [ 0, 1, 0, -1 ]
def getValue(offset: int, signal: List[int]) -> int:
    total = 0
    for index, number in enumerate(signal):
        indexInPattern = ((index + 1) // offset) % len(PATTERN)
        multiplier = PATTERN[ indexInPattern ]
        total += number * multiplier
    return abs(total) % 10


def nextPhase(signal: List[int]) -> List[int]:
    result = []
    for index in range(len(signal)):
        result.append(getValue(index + 1, signal))
    return result


def part1(signal: List[int]) -> str:
    signal = list(signal)
    for _ in range(100):
        signal = nextPhase(signal)
    return "".join([ str(n) for n in signal[:8] ])


def part2(signal: List[int]) -> str:
    offset = int("".join(map(str, signal[:7])))
    signal = (signal*10000)[offset:]
    for _ in range(100):
        sum = 0
        for i in range(len(signal)-1, -1, -1):
            signal[i] = sum = (sum + signal[i]) % 10
    return "".join(map(str, signal[:8]))


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(c) for c in file.read().strip() ]


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()