#! /usr/bin/python3

import sys, os, time
import re


def isPossibleTriangle(sideA, sideB, sideC):
    return sideA < (sideB + sideC) \
            and sideB < (sideA + sideC) \
            and sideC < (sideA + sideB)


def part1(triangleSides):
    return sum([ isPossibleTriangle(sideA, sideB, sideC) for sideA, sideB, sideC in triangleSides ])


def part2(triangleSides):
    return sum(
        [ sum([ isPossibleTriangle( \
                triangleSides[rowIndex * 3][columnIndex], \
                triangleSides[rowIndex * 3 + 1][columnIndex], \
                triangleSides[rowIndex * 3 + 2][columnIndex]) \
                for columnIndex in range(3) ]) \
            for rowIndex in range(len(triangleSides) // 3)
        ])


lineRegex = re.compile(r"\d+")
def parseLine(line):
    return [ int(i) for i in  lineRegex.findall(line) ]


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