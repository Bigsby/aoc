#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple


def getNthTurn(numbers: List[int], turns: int) -> int:
    turn = 0
    occurrences: Dict[int,Tuple[int,int]] = {}
    for number in numbers:
        turn += 1
        occurrences[number] = (turn, 0)
    lastNumber = numbers[-1]
    while turn < turns:
        turn += 1
        lastOccurrence, secondLastOccurence = occurrences[lastNumber]
        if secondLastOccurence == 0:
            lastNumber = 0
        else:
            lastNumber = lastOccurrence - secondLastOccurence
        if lastNumber in occurrences:
            occurrences[lastNumber] = (turn, occurrences[lastNumber][0])
        else:
            occurrences[lastNumber] = (turn, 0)
    return lastNumber


def part1(numbers: List[int]) -> int:
    return getNthTurn(numbers, 2020)


def part2(numbers: List[int]) -> int:
    return getNthTurn(numbers, 30000000)


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().split(",") ]


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