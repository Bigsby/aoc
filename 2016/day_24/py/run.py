#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from itertools import permutations

Location = complex
Maze = List[complex]
DIRECTIONS = [ -1, -1j, 1, 1j ]


def findPathsFromLocation(maze: Maze, numbers: Dict[Location, int], start: Location) -> Dict[int,int]:
    visited = { start }
    queue: List[Tuple[int,int,int]] = [ (int(start.real), int(start.imag), 0) ]
    paths: Dict[int,int] = {}
    while queue:
        x, y, distance = queue.pop(0)
        for direction in DIRECTIONS:
            newPosition = x + y * 1j + direction
            if newPosition in maze and newPosition not in visited:
                visited.add(newPosition)
                if newPosition in numbers:
                    paths[numbers[newPosition]] = distance + 1
                queue.append((int(newPosition.real), int(newPosition.imag), distance + 1))
    return paths


def getStepsForPath(path: List[int], pathsFromNumbers: Dict[int,Dict[int,int]]) -> int:
    steps = 0
    current = 0
    while path:
        next = path.pop(0)
        steps += pathsFromNumbers[current][next]
        current = next
    return steps


def findLeastSteps(data: Tuple[Maze,Dict[Location,int]], returnHome: bool) -> int:
    maze, numbers = data
    pathsFromNumbers = { number: findPathsFromLocation(maze, numbers, location) for location, number in numbers.items() }
    numbersBesidesStart = [ number for number in numbers.values() if number != 0 ]
    minumSteps = sys.maxsize
    for combination in permutations(numbersBesidesStart, len(numbersBesidesStart)):
        steps = getStepsForPath(list(combination) + ([ 0 ] if returnHome else []), pathsFromNumbers)
        minumSteps = min(minumSteps, steps)
    return minumSteps


def part1(data: Tuple[Maze,Dict[Location,int]]):
    return findLeastSteps(data, False)


def part2(data: Tuple[Maze,Dict[Location,int]]):
    return findLeastSteps(data, True)


def getInput(filePath: str) -> Tuple[Maze,Dict[Location,int]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        maze = []
        numbers = {}
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

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()