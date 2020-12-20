#! /usr/bin/python3

from functools import reduce

from common import getInput


def doSidesMatch(thisSides, otherSides):
    for side in thisSides:
        for otherSide in otherSides:
            if side == otherSide or side == otherSide[::-1]:
                return True
    return False


def findMatchingBorders(tile, tiles):
    count = 0
    for otherTile in tiles:
        if otherTile.number == tile.number:
            continue
        if doSidesMatch(tile.borders, otherTile.borders):
            count += 1
        
    return count



def main():
    tiles = list(getInput())
    tileCounts = {}
    
    for tile in tiles:
        tileCounts[tile.number] = findMatchingBorders(tile, tiles)

    corners = [ tileNumber for tileNumber in tileCounts if tileCounts[tileNumber] == 2 ]
    result = reduce(lambda soFar, tileNumber: soFar * tileNumber, corners)
    print("Corners product:", result)

    


if __name__ == "__main__":
    main()
