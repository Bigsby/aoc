#! /usr/bin/python3

import sys, os, time


def getNthTurn(numbers, turns):
    turn = 0
    occurrences = {}
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
            lastNumberOccurrence, _ = occurrences[lastNumber]
            occurrences[lastNumber] = (turn, lastNumberOccurrence)
        else:
            occurrences[lastNumber] = (turn, 0)

    return lastNumber


def part1(puzzleInput):
    return getNthTurn(puzzleInput, 2020)


def part2(puzzleInput):
    return getNthTurn(puzzleInput, 30000000)


def getInput(filePath):
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()