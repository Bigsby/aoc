#! /usr/bin/python3

from common import getInput, flipInitialTiles, steps, getTotalBlackCount

def getNeighbors(tile):
    for _, step in steps.items():
        yield (tile[0] + step[0], tile[1] + step[1], tile[2] + step[2])


def getBlackCount(neighbors, tiles):
    return sum([ 1 for neighbor in neighbors if neighbor in tiles and tiles[neighbor] ])

def getTileState(tile, tiles):
    return tile in tiles and tiles[tile]

def getNewState(tile, tiles):
    neighbors = list(getNeighbors(tile))
    adjacentBlackCount = getBlackCount(neighbors, tiles)
    tileState = getTileState(tile, tiles)
    if tileState and adjacentBlackCount == 0 or adjacentBlackCount > 2:
        return False
    return (not tileState and adjacentBlackCount == 2) or tileState


def runDay(tiles):
    newState = {}
    edgesToTest = set()
    for tile in tiles:
        neighbors = list(getNeighbors(tile))
        edgesToTest.update({ neighbor for neighbor in neighbors if neighbor not in tiles })
        newState[tile] = getNewState(tile, tiles)
    for tile in edgesToTest:
        newState[tile] = getNewState(tile, tiles)

    return newState


def main():
    tilePaths = list(getInput())
    tiles = flipInitialTiles(tilePaths)

    day = 0
    while day < 100:
        day += 1
        tiles = runDay(tiles)

    result = sum([tiles[position] for position in tiles if tiles[position] ])
    print("Black tiles count:", result)


if __name__ == "__main__":
    main()
