#! /usr/bin/python3

import sys, os, time
from typing import Tuple
from collections import Counter


def isValidPassword(password: str, check2: bool) -> bool:
    if "".join(list(sorted(list(password)))) == password:
        counts = Counter(password).values()
        return any([ count > 1 for count in counts ]) and (2 in counts or not check2)
    return False


def getValidPasswordCount(limits: Tuple[int,int], check2: bool) -> int:
    start, end = limits
    return sum([ isValidPassword(str(password), check2) for password in range(start, end) ])


def solve(limits: Tuple[int,int]) -> Tuple[int,int]:
    return (
        getValidPasswordCount(limits, False),
        getValidPasswordCount(limits, True)
    )


def getInput(filePath: str) -> Tuple[int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        split = file.read().split("-")
        return (int(split[0]), int(split[1]))


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