#! /usr/bin/python3

import sys, os, time
from itertools import combinations


def part1(puzzleInput):
    for number in puzzleInput:
        numberToFind = 2020 - number
        if numberToFind in puzzleInput:
            return number * numberToFind


def part2(puzzleInput):
    for combination in combinations(puzzleInput, 2):
        numberA, numberB = combination
        numberToFind = 2020 - numberA - numberB
        if numberToFind in puzzleInput:
            return numberA * numberB * numberToFind


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(line) for line in file.readlines() ]


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