#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


def isPositionValid(position: complex, number: int) -> bool:
    x, y = int(position.real), int(position.imag)
    if x < 0 or y < 0:
        return False
    value = x*x + 3*x + 2*x*y + y + y*y + number
    return f"{value:b}".count("1") % 2 == 0


DIRECTIONS = [ -1, 1j, -1j, 1]
def solve(number: int) -> Tuple[int,int]:
    startPosition = 1 + 1j
    queue: List[Tuple[complex,List[complex]]] = [(startPosition, [startPosition])]
    allVisited = { startPosition }
    part1Result = 0
    target = 31 + 39 * 1j
    while queue and part1Result == 0:
        position, visited = queue.pop(0)
        for direction in DIRECTIONS:
            newPosition = position + direction
            if newPosition == target:
                part1Result = len(visited)
            if newPosition not in visited and isPositionValid(newPosition, number):
                if (len(visited) <= 50):
                    allVisited.add(newPosition)
                newVisited = list(visited)
                newVisited.append(newPosition)
                queue.append((newPosition, newVisited))
    return part1Result, len(allVisited)


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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