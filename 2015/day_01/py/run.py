#! /usr/bin/python3

import sys, os, time


def part1(puzzleInput):
    currentFloor = 0
    for direction in puzzleInput:
        currentFloor = currentFloor + direction

    return currentFloor


def part2(puzzleInput):
    currentFloor = 0
    currentPosition = 1
    for direction in puzzleInput:
        currentFloor = currentFloor + direction
        if currentFloor == -1:
            break
        currentPosition = currentPosition + 1

    return currentPosition


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath) as file:
        return [ 1 if c == "(" else -1 for c in file.read() ]


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