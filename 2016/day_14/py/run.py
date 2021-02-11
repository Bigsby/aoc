#! /usr/bin/python3

import sys, os, time
from typing import Dict, List
import re
from hashlib import md5


tripletRegex = re.compile(r"(.)\1{2}")
quintetRegex = re.compile(r"(.)\1{4}")
def findKey(salt: str, stretch: int) -> int:
    index = 0
    keys: List[int] = []
    threes: Dict[str,List[int]] = { digit: [] for digit in "0123456789abcdef" }
    while len(keys) < 64:
        value = salt + str(index)
        for _ in range(stretch + 1):
            value = md5(value.encode()).hexdigest()
        match = quintetRegex.search(value)
        if match:
            digit = match.group()[0]
            for tripletIndex in threes[digit]:
                if (index - tripletIndex) <= 1000:
                    keys.append(tripletIndex)
            threes[digit] = []

        match = tripletRegex.search(value)
        if match:
            threes[match.group()[0]].append(index)
        index += 1

    keys.sort()
    return keys[63]


def part1(salt: str) -> int:
    return findKey(salt, 0)


def part2(salt: str) -> int:
    return findKey(salt, 2016)


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()