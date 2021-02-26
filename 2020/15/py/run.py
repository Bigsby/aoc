#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple


def solve(numbers: List[int]) -> Tuple[int,int]:
    part1Result = 0
    turn = 0
    occurrences: Dict[int,Tuple[int,int]] = {}
    for number in numbers:
        turn += 1
        occurrences[number] = (turn, 0)
    lastNumber = numbers[-1]
    while turn < 30_000_000:
        if turn == 2020:
            part1Result = lastNumber
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
    return part1Result, lastNumber


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().split(",") ]


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