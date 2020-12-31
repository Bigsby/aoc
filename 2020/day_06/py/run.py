#! /usr/bin/python3

import sys, os, time
from functools import reduce


def countGroupAnswers(group):
    _, record = group
    return sum(map(lambda letter: record[letter] != 0, record.keys()))


def part1(puzzleInput):
    return sum(map(lambda group: countGroupAnswers(group), puzzleInput))


def getGroupCommonAnswers(group):
    peopleCount, record = group
    return sum(map(lambda letter: record[letter] == peopleCount, record.keys()))


def part2(puzzleInput):
    return sum(map(lambda group: getGroupCommonAnswers(group), puzzleInput))


def addToLetterCount(record, letter):
    if letter in record:
        record[letter] = record[letter] + 1
    else:
        record[letter] = 1


def processEntry(entry):
    record = {}
    peopleCount = 0
    for line in entry.split("\n"):
        if line:
            peopleCount = peopleCount + 1
        for c in line:
            addToLetterCount(record, c)
    return (peopleCount, record)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ processEntry(entry) for entry in file.read().split("\n\n") ]


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