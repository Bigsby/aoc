#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def runCycles(numbers: List[int]) -> Tuple[int, int]:
    numbersLength = len(numbers)
    prevousLists: List[str] = []
    cycles = 0
    currentList = list(numbers)
    while True:
        currentListStr = ",".join(map(str, currentList))
        if currentListStr in prevousLists:
            return cycles, prevousLists.index(currentListStr)
        cycles += 1
        prevousLists.append(currentListStr)

        updateIndex = -1
        maxNumber = 0
        for index, number in enumerate(currentList):
            if number > maxNumber:
                maxNumber = number
                updateIndex = index

        currentList[updateIndex] = 0
        while maxNumber:
            updateIndex = updateIndex + 1 if updateIndex < numbersLength - 1 else 0
            currentList[updateIndex] += 1
            maxNumber -= 1
        

def part1(numbers: List[int]) -> int:
    return runCycles(numbers)[0]


def part2(numbers: List[int]) -> int :
    cycles, first = runCycles(numbers)
    return cycles - first    


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().split("\t") ]


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