#! /usr/bin/python3

import sys, os, time
from typing import List

Tiles = List[bool]


def getSafeCount(tiles: Tiles, count: int) -> int:
    safe = sum(tiles)
    for _ in range(1, count):
        tiles = [True] + tiles + [True]
        tiles = [left == right for left, right in zip(tiles, tiles[2:])]
        safe += sum(tiles)
    return safe


def part1(tiles: Tiles) -> int:
    return getSafeCount(tiles, 40)


def part2(tiles: Tiles) -> int:
    return getSafeCount(tiles, 400_000)


def getInput(filePath: str) -> Tiles:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return list(c == "." for c in file.read().strip())


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