#! /usr/bin/python3

import sys, os, time
from hashlib import md5
from typing import Tuple


def findHash(secretKey: str, prefixCount: int, guess: int) -> int:
    prefix = "0" * prefixCount
    while True:
        result = md5((secretKey + str(guess)).encode("utf-8")).hexdigest()
        if result.startswith(prefix):
            break
        guess += 1
    return guess


def solve(secretKey: str) -> Tuple[int,int]:
    part1Result = findHash(secretKey, 5, 1)
    return (part1Result, findHash(secretKey, 6, part1Result))


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()