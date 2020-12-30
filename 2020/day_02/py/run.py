#! /usr/bin/python3

import sys, os, time
import re


def countValid(puzzleInput, validationFunc):
    return len([ 1 for line in puzzleInput if validationFunc(line) ])


def isLineValid(line):
    minimum, maximum, letter, password = line
    occurenceCount = password.count(letter) 
    return occurenceCount >= minimum and occurenceCount <= maximum


def part1(puzzleInput):
    return countValid(puzzleInput, isLineValid)


def isLineValid2(line):
    first, second, letter, password = line 
    return (password[first - 1] == letter) ^ (password[second - 1] == letter)


def part2(puzzleInput):
    return countValid(puzzleInput, isLineValid2)


lineReEx = re.compile("^(\d+)-(\d+)\s([a-z]):\s(.*)$")
def parseLine(line):
    match = lineReEx.match(line)
    min, max, letter, password = match.group(1, 2, 3, 4)
    return (int(min), int(max), letter, password)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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