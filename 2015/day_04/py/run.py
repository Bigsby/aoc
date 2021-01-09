#! /usr/bin/python3

import sys, os, time
from hashlib import md5


def findHash(secretKey: str, prefixCount: int) -> int:
    prefix = "0" * prefixCount
    guess = 1
    while True:
        result = md5((secretKey + str(guess)).encode("utf-8")).hexdigest()
        if result.startswith(prefix):
            break
        guess = guess + 1
    return guess


def part1(secretKey: str) -> int:
    return findHash(secretKey, 5)


def part2(secretKey: str) -> int:
    return findHash(secretKey, 6)


def getInput(filePath: str) -> str:
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