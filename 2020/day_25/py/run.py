#! /usr/bin/python3

import sys, os, time
from typing import Tuple


BASE_SUBJECT_NUMBER = 7
DIVIDER = 20201227
def getNextValue(value: int, subjectNumber: int = BASE_SUBJECT_NUMBER) -> int:
    return (value * subjectNumber) % DIVIDER


def getLoopSize(target: int) -> int:
    value = 1
    cycle = 0
    while value != target:
        cycle += 1
        value = getNextValue(value)
    return cycle


def transform(subjectNumber: int, cycles: int) -> int:
    value = 1
    while cycles:
        cycles -= 1
        value = getNextValue(value, subjectNumber)
    return value


def part1(puzzleInput: Tuple[int,...]) -> int:
    card, door = puzzleInput
    return transform(card, getLoopSize(door))


def part2(_):
    pass


def getInput(filePath: str) -> Tuple[int,...]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return  tuple(int(line.strip()) for line in file.readlines())


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