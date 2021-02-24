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


def part1(limits: Tuple[int,int]) -> int:
    return getValidPasswordCount(limits, False)


def part2(limits: Tuple[int,int]) -> int:
    return getValidPasswordCount(limits, True)


def getInput(filePath: str) -> Tuple[int,int]:
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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()