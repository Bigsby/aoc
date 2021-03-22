#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple
from itertools import permutations

Location = complex
Maze = List[complex]


DIRECTIONS = [-1, -1j, 1, 1j]


def findPathsFromLocation(maze: Maze, numbers: Dict[Location, int], start: Location) -> Dict[int, int]:
    visited = {start}
    queue: List[Tuple[complex, int]] = [(start, 0)]
    paths: Dict[int, int] = {}
    while queue:
        position, distance = queue.pop(0)
        for direction in DIRECTIONS:
            newPosition = position + direction
            if newPosition in maze and newPosition not in visited:
                visited.add(newPosition)
                if newPosition in numbers:
                    paths[numbers[newPosition]] = distance + 1
                queue.append((newPosition, distance + 1))
    return paths


def getStepsForPath(path: Iterable[int], pathsFromNumbers: Dict[int, Dict[int, int]], returnHome: bool) -> int:
    steps = 0
    current = 0
    pathList = list(path)
    while pathList:
        next = pathList.pop(0)
        steps += pathsFromNumbers[current][next]
        current = next
    if returnHome:
        steps += pathsFromNumbers[current][0]
    return steps


def solve(data: Tuple[Maze, Dict[Location, int]]) -> Tuple[int, int]:
    maze, numbers = data
    pathsFromNumbers = {number: findPathsFromLocation(
        maze, numbers, location) for location, number in numbers.items()}
    numbersBesidesStart = [
        number for number in numbers.values() if number != 0]
    pathCombinations = list(permutations(
        numbersBesidesStart, len(numbersBesidesStart)))
    minimumSterps = sys.maxsize
    returnMinimumSteps = sys.maxsize
    for combination in pathCombinations:
        minimumSterps = min(minimumSterps, getStepsForPath(
            combination, pathsFromNumbers, False))
        returnMinimumSteps = min(returnMinimumSteps, getStepsForPath(
            combination, pathsFromNumbers, True))
    return minimumSterps, returnMinimumSteps


def getInput(filePath: str) -> Tuple[Maze, Dict[Location, int]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        maze = Maze()
        numbers: Dict[Location, int] = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                location = x + y * 1j
                if c == ".":
                    maze.append(location)
                elif c.isdigit():
                    numbers[location] = int(c)
                    maze.append(location)
        return maze, numbers


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
