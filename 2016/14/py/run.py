#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
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


def solve(salt: str) -> Tuple[int,int]:
    return (
        findKey(salt, 0),
        findKey(salt, 2016)
    )


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