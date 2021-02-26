#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

Position = complex
Tubes = List[Position]
Letters = Dict[Position,str]


def solve(data: Tuple[Tubes,Letters,Position]) -> Tuple[str,int]:
    tubes, letters, currentPosition = data
    path = []
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


TUBES = [ "|", "+", "-" ]
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
                if c in TUBES:
                    tubes.append(position)
                    if y == 0:
                        start = position
                if "A" <= c <= "Z":
                    letters[position] = c
                    tubes.append(position)        
        return tubes, letters, start


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