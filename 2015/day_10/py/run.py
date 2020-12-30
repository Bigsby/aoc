#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce


testRegex = re.compile(r"(\d)\1+|\d")
def getNextValue(value):
    matches = testRegex.finditer(value)
    sequences = []
    for match in matches:
        group = match.group()
        sequences.append(str(len(group)))
        sequences.append(group[0])
    return "".join(sequences)


def runLookAndSay(puzzleInput, turns):
    currentValue = puzzleInput
    for _ in range(0, turns):
        currentValue = getNextValue(currentValue)
    return len(currentValue)


def part1(puzzleInput):
    return runLookAndSay(puzzleInput, 40)


def part2(puzzleInput):
    return runLookAndSay(puzzleInput, 50)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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