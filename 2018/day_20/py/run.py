#! /usr/bin/python3

import sys, os, time
from collections import defaultdict
from typing import Dict, Iterable


DIRECTIONS = {
    "N": 1j,
    "S": -1j,
    "E": 1,
    "W": -1
}
def getDistances(routes: str) -> Iterable[int]:
    distances: Dict[complex,int] = defaultdict(lambda:sys.maxsize)
    distances[0j] = 0
    groupEnds = []
    head = 0j
    for c in routes[1:-1]:
        if c == "(":
            groupEnds.append(head)
        elif c == ")":
            head = groupEnds.pop()
        elif c == "|":
            head = groupEnds[-1]
        else:
            previous = head
            head += DIRECTIONS[c]
            distances[head] = min(distances[head], distances[previous] + 1)
    return distances.values()


def part1(routes: str) -> int:
    return max(getDistances(routes))


def part2(routes: str) -> int:
    return sum(1 for distance in getDistances(routes) if distance >= 1000)


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