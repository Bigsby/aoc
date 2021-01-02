#! /usr/bin/python3

import sys, os, time


baseSubjectNumber = 7
divider = 20201227
def getNextValue(value, subjectNumber = baseSubjectNumber):
    return (value * subjectNumber) % divider


def getLoopSize(target):
    value = 1
    cycle = 0
    while value != target:
        cycle += 1
        value = getNextValue(value)
    return cycle


def transform(subjectNumber, cycles):
    value = 1
    while cycles:
        cycles -= 1
        value = getNextValue(value, subjectNumber)
    return value


def part1(puzzleInput):
    card, door = puzzleInput
    return transform(card, getLoopSize(door))


def part2(_):
    pass


def getInput(filePath):
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()