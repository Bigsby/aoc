#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

Position = complex
Tubes = List[Position]
Letters = Dict[Position,str]


def followPath(data: Tuple[Tubes,Letters,Position]) -> Tuple[str,int]:
    tubes, letters, start = data
    path = []
    currentPosition = start
    direction = 1j
    steps = 0
    while True:
        steps += 1
        if currentPosition in letters:
            path.append(letters[currentPosition])
        if currentPosition + direction in tubes:
            currentPosition += direction
        elif currentPosition + direction * 1j in tubes:
            direction *= 1j
            currentPosition += direction
        elif currentPosition + direction * -1j in tubes:
            direction *= -1j
            currentPosition += direction
        else:
            break

    return "".join(path), steps


def part1(data: Tuple[Tubes,Letters,Position]) -> str:
    letters, _ = followPath(data)
    return letters


def part2(data: Tuple[Tubes,Letters,Position]) -> int:
    _, steps = followPath(data)
    return steps


def getInput(filePath: str) -> Tuple[Tubes,Letters,Position]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        tubes = []
        letters = {}
        start = -1j
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line):
                position = x + y * 1j
                if c in [ "|", "+", "-" ]:
                    tubes.append(position)
                    if y == 0:
                        start = position
                if ord("A") <= ord(c) <= ord("Z"):
                    letters[position] = c
                    tubes.append(position)
        
        return tubes, letters, start


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