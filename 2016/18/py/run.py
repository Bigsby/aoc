#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple

Tiles = List[bool]


def solve(tiles: Tiles) -> Tuple[int,int]:
    safe = sum(tiles)
    part1Result = 0
    for step in range(1, 400_000):
        if step == 40:
            part1Result = safe
        tiles = [True] + tiles + [True]
        tiles = [left == right for left, right in zip(tiles, tiles[2:])]
        safe += sum(tiles)
    return part1Result, safe


def getInput(filePath: str) -> Tiles:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return list(c == "." for c in file.read().strip())


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