#! /usr/bin/python3

import sys, os, time
from hashlib import md5

PREFIX = "0" * 5
ENCODING = "utf-8"


def part1(doorId: str) -> str:
    index = 0
    password = ""
    while len(password) < 8:
        result = md5((doorId + str(index)).encode(ENCODING)).hexdigest()
        if result.startswith(PREFIX):
            password += result[5]
        index += 1
    return password


def part2(doorId: str) -> str:
    index = 0
    password = [ "_" for _ in range(8) ]
    missingIndexes = list("01234567")
    while missingIndexes:
        result = md5((doorId + str(index)).encode(ENCODING)).hexdigest()
        if result.startswith(PREFIX):
            digitIndex = result[5]
            if digitIndex in missingIndexes:
                password[int(digitIndex)] = result[6]
                missingIndexes.remove(digitIndex)
        index += 1
    return "".join(password)


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read()


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