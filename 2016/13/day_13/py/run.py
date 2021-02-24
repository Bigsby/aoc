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


def part1(number: int) -> int:
    startPosition = 1 + 1j
    queue: List[Tuple[complex,List[complex]]] = [(startPosition, [startPosition])]
    target = 31 + 39 * 1j
    while queue:
        position, visited = queue.pop(0)
        for direction in DIRECTIONS:
            newPosition = position + direction
            if newPosition == target:
                return len(visited)
            if newPosition not in visited and isPositionValid(newPosition, number):
                newVisited = list(visited)
                newVisited.append(newPosition)
                queue.append((newPosition, newVisited))

    raise Exception("Path not found")


def part2(number: int) -> int:
    startPosition = 1 + 1j
    queue: List[Tuple[complex,List[complex]]] = [(startPosition, [startPosition])]
    allVisited = { startPosition }
    while queue:
        position, visited = queue.pop(0)
        if len(visited) <= 50:
            for direction in DIRECTIONS:
                newPosition = position + direction
                if newPosition not in visited and isPositionValid(newPosition, number):
                    allVisited.add(newPosition)
                    newVisited = list(visited)
                    newVisited.append(newPosition)
                    queue.append((newPosition, newVisited))
    return len(allVisited)


def getInput(filePath: str) -> int:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return int(file.read().strip())


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