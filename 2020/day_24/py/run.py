#! /usr/bin/python3

import sys, os, time
import re


STEPS = {
    "e": (1,-1,0),
    "se": (0,-1,1),
    "sw": (-1,0,1),
    "w": (-1,1,0),
    "nw": (0,1,-1),
    "ne": (1,0,-1)
}


def flipInitialTiles(tilePaths):
    tiles = {}
    for path in tilePaths:
        current = (0,0,0)
        for direction in path:
            step = STEPS[direction]
            current = current[0] + step[0], current[1] + step[1], current[2] + step[2]
        if current in tiles:
            tiles[current] = not tiles[current]
        else:
            tiles[current] = True
    return tiles


def getTotalBlackCount(tiles):
    return sum([tiles[position] for position in tiles if tiles[position] ])


def part1(tilePaths):
    tiles = flipInitialTiles(tilePaths)
    return getTotalBlackCount(tiles)


def getNeighbors(tile):
    tileX, tileY, tileZ = tile
    return [ (tileX + stepX, tileY + stepY, tileZ + stepZ) for stepX, stepY, stepZ in STEPS.values() ]


def getBlackCount(neighbors, tiles):
    return sum([ 1 for neighbor in neighbors if neighbor in tiles and tiles[neighbor] ])


def getTileState(tile, tiles):
    return tile in tiles and tiles[tile]


def getNewState(tile, tiles):
    adjacentBlackCount = getBlackCount(getNeighbors(tile), tiles)
    tileState = getTileState(tile, tiles)
    if tileState and adjacentBlackCount == 0 or adjacentBlackCount > 2:
        return False
    return (not tileState and adjacentBlackCount == 2) or tileState


def runDay(tiles):
    newState = {}
    edgesToTest = set()
    for tile in tiles:
        edgesToTest.update({ neighbor for neighbor in getNeighbors(tile) if neighbor not in tiles })
        newState[tile] = getNewState(tile, tiles)
    for tile in edgesToTest:
        newState[tile] = getNewState(tile, tiles)

    return newState


def part2(tilePaths):
    tiles = flipInitialTiles(tilePaths)
    day = 0
    while day < 100:
        day += 1
        tiles = runDay(tiles)
    return sum([tiles[position] for position in tiles if tiles[position] ])


lineRegex = re.compile(r"e|se|sw|w|nw|ne")
def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ lineRegex.findall(line.strip()) for line in file.readlines() ]


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