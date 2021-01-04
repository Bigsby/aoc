#! /usr/bin/python3

import sys, os, time
from collections import Counter


def isValidPassword(password, check2):
    if "".join(sorted(password)) == password:
        counts = Counter(password).values()
        return any([ count > 1 for count in counts ]) and 2 in counts or not check2
    return False


def getValidPasswordCount(limits, check2):
    start, end = limits
    return sum([ isValidPassword(str(password), check2) for password in range(start, end) ])


def part1(limits):
    return getValidPasswordCount(limits, False)


def part2(limits):
    return getValidPasswordCount(limits, True)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        split = file.read().split("-")
        return (int(split[0]), int(split[1]))


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