#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from hashlib import md5


DIRECTIONS = {
    "U": 1j,
    "D": -1j,
    "L": -1,
    "R": 1
}
def solve(passcode: str) -> Tuple[str,int]:
    queue: List[Tuple[complex,str]] = [(0j, "")]
    longestPathFound = 0
    shortestPath = ""
    while queue:
        room, path = queue.pop(0)
        if room == 3 - 3j:
            if not shortestPath:
                shortestPath = path
            longestPathFound = max(longestPathFound, len(path))
            continue
        pathHash = md5((passcode + path).encode("utf-8")).hexdigest()[:4]
        for index, (pathLetter, direction) in enumerate(DIRECTIONS.items()):
            newRoom = room + direction
            if pathHash[index] > "a" and 0 <= newRoom.real < 4 and -4 < newRoom.imag <= 0:
                queue.append((room + direction, path + pathLetter))
    return shortestPath, longestPathFound


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