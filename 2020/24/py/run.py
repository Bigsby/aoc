#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple
import re

Directions = List[str]
Tile = complex
Floor = Dict[Tile, bool]
DIRECTIONS = {
    "e":   1,
    "se":      1j,
    "sw": -1 + 1j,
    "w": -1,
    "ne":  1 - 1j,
    "nw": - 1j
}


def flipInitialTiles(tilePaths: List[Directions]) -> Floor:
    floor = Floor()
    for path in tilePaths:
        current = 0
        for direction in path:
            current += DIRECTIONS[direction]
        if current in floor:
            floor[current] = not floor[current]
        else:
            floor[current] = True
    return floor


def getNeighbors(tile: Tile) -> List[Tile]:
    return [tile + direction for direction in DIRECTIONS.values()]


def getBlackCount(neighbors: List[Tile], floor: Floor) -> int:
    return sum([1 for neighbor in neighbors if neighbor in floor and floor[neighbor]])


def getTileState(tile: Tile, floor: Floor) -> bool:
    return tile in floor and floor[tile]


def getNewState(tile: Tile, floor: Floor) -> bool:
    adjacentBlackCount = getBlackCount(getNeighbors(tile), floor)
    tileState = getTileState(tile, floor)
    if tileState and adjacentBlackCount == 0 or adjacentBlackCount > 2:
        return False
    return (not tileState and adjacentBlackCount == 2) or tileState


def runDay(floor: Floor) -> Floor:
    newFloor = Floor()
    edgesToTest: Set[Tile] = set()
    for tile in floor:
        edgesToTest.update(
            {neighbor for neighbor in getNeighbors(tile) if neighbor not in floor})
        newFloor[tile] = getNewState(tile, floor)
    for tile in edgesToTest:
        newFloor[tile] = getNewState(tile, floor)
    return newFloor


def part2(floor: Floor) -> int:
    for _ in range(100):
        floor = runDay(floor)
    return sum(floor.values())


def solve(tilePaths: List[Directions]) -> Tuple[int, int]:
    floor = flipInitialTiles(tilePaths)
    return (
        sum(floor.values()),
        part2(floor)
    )


lineRegex = re.compile(r"e|se|sw|w|nw|ne")


def getInput(filePath: str) -> List[Directions]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        return [lineRegex.findall(line.strip()) for line in file.readlines()]


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
