#! /usr/bin/python3

import sys, os, time
from typing import Dict, Iterable, Tuple
from collections import defaultdict


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


def solve(routes: str) -> Tuple[int,int]:
    distances = getDistances(routes)
    return (
        max(distances),
        sum(1 for distance in distances if distance >= 1000)
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