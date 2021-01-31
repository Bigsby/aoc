#! /usr/bin/python3

import sys, os, time
from typing import Dict, List
from collections import defaultdict

Bug = complex
Bugs = List[Bug]
DIRECTIONS = [ 1, -1, 1j, -1j ]


def getsBug(hasBug: bool, adjacentCount: int) -> bool:
    return adjacentCount == 1 if hasBug else adjacentCount in (1, 2)


def nextMinute(bugs: Bugs) -> Bugs:
    newState = []
    for y in range(5):
        for x in range(5):
            position = x + y * 1j
            adjacentCount = sum(offset + position in bugs for offset in DIRECTIONS)
            if getsBug(position in bugs, adjacentCount):
                newState.append(position)
    return newState


def part1(bugs: Bugs) -> int:
    previous = [ bugs ]
    while True:
        bugs = nextMinute(bugs)
        if bugs in previous:
            break
        previous.append(bugs)
    biodiversity = 0
    for y in range(5):
        for x in range(5):
            if x + y * 1j in bugs:
                biodiversity += 1 << (y * 5 + x)
    return biodiversity


def nextLayeredMinute(layers: Dict[int,Bugs]) -> Dict[int,Bugs]:
    newState: Dict[int,Bugs] = defaultdict(list)
    for layer in range(min(layers.keys()) - 1, max(layers.keys()) + 2):
        for y in range(5):
            for x in range(5):
                position = x + y * 1j
                if position == 2 + 2j:
                    continue

                adjacentCount = sum(offset + position in layers[layer] for offset in DIRECTIONS)
                if y == 0:
                    adjacentCount += 2 + 1j in layers[layer - 1]
                elif y == 4:
                    adjacentCount += 2 + 3j in layers[layer - 1]
                
                if x == 0:
                    adjacentCount += 1 + 2j in layers[layer - 1]
                elif x == 4:
                    adjacentCount += 3 + 2j in layers[layer - 1]

                if position == 2 + 1j:
                    adjacentCount += sum(x in layers[layer + 1] for x in range(5))
                elif position == 1 + 2j:
                    adjacentCount += sum(y * 1j in layers[layer + 1] for y in range(5))
                elif position == 3 + 2j:
                    adjacentCount += sum(4 + y * 1j in layers[layer + 1] for y in range(5))
                elif position == 2 + 3j:
                    adjacentCount += sum(x + 4j in layers[layer + 1] for x in range(5))
                if getsBug(position in layers[layer], adjacentCount):
                    newState[layer].append(position)
    return newState


def part2(bugs: Bugs) -> int:
    layers: Dict[int,Bugs] = defaultdict(list)
    layers[0] = bugs
    minutes = 0
    for _ in range(200):
        minutes += 1
        layers = nextLayeredMinute(layers)
    return sum(len(bugs) for bugs in layers.values())



def getInput(filePath: str) -> Bugs:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        bugs: Bugs = []
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                if c == "#":
                    bugs.append(x + y * 1j)
        return bugs
                

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