#! /usr/bin/python3

from functools import reduce

from common import getInput


def doSidesMatch(thisSides, otherSides):
    for thisIndex, side in enumerate(thisSides):
        for otherIndex, otherSide in enumerate(otherSides):
            if side == otherSide:
                return True, thisIndex, otherIndex, False
            if side == otherSide or side == otherSide[::-1]:
                return True, thisIndex, otherIndex, True
    return False, 0, 0, False


class TileConnection():
    def __init__(self, tile1, tile2, side1, side2, flipped):
        self.tile1 = tile1
        self.tile2 = tile2
        self.side1 = side1
        self.side2 = side2
        self.flipped = flipped

    def __str__(self):
        return f"{self.tile1}-{self.side1} > {self.tile2}-{self.side2}"
    def __repr__(self):
        return self.__str__()



class PuzzleTile():
    def __init__(self, number, rotate, flipped):
        self.number = number
        self.rotate = rotate
        self.flipped = flipped
    def __str__(self):
        return f"{self.number}"
    def __repr__(self):
        return self.__str__()


def findMatchingBorders(tile, tiles):
    count = 0
    connections = []
    for otherTile in tiles:
        if otherTile.number == tile.number:
            continue
        matched, thisSide, otherSide, flipped = doSidesMatch(tile.borders, otherTile.borders)
        if matched:
            connections.append(TileConnection(tile.number, otherTile.number, thisSide, otherSide, flipped))
            count += 1
        
    return count, connections


def getTopLeftTile(corners, connections):
    for corner in corners:
        hasRightConnection = any(map(lambda connection: connection.tile1 == corner and connection.side1 == 1, connections))
        hasDownConnection = any(map(lambda connection: connection.tile1 == corner and connection.side1 == 2, connections))
        if hasRightConnection and hasDownConnection:
            return corner

def main():
    tiles = list(getInput())
    tileCounts = {}
    connections = []
    
    for tile in tiles:
        count, tileConnections = findMatchingBorders(tile, tiles)
        tileCounts[tile.number] = count
        connections += tileConnections

    for connection in connections:
        print(connection)

    corners = [ tileNumber for tileNumber in tileCounts if tileCounts[tileNumber] == 2 ]
    print("corners:", corners)

    puzzle = [[]]
    currentTile = PuzzleTile(getTopLeftTile(corners, connections), 0, False)
    direction = 1, 3
    currentRow = 0
    puzzle[currentRow].append(currentTile)
    print(currentTile)
    turnCorner = True

    while len(connections):
        print()
        print(connections)
        print(puzzle)
        print(currentTile, ">", direction)
        connection = next((c for c in connections if c.tile1 == currentTile.number and (c.side1 == direction[0] or c.side == direction[1]), None)
        input(connection)
        if connection:
            newTile = PuzzleTile(connection.tile2, 0, False)
            if direction == 1 or direction == 2:
                puzzle[currentRow].append(newTile)
            else:
                puzzle[currentRow].insert(0, newTile)
            if turnCorner:
                direction = (1, 3)
                print("D changed direciton to", direction)
                turnCorner = 0
            connections = list(filter(lambda c: c.tile1 != currentTile.number and c.tile2 != newTile.number, connections))
            currentTile = newTile
        else:
            puzzle.append([])
            currentRow += 1
            direction = (2, 0)
            tir
            print("changed direction to", direction)

    print(puzzle)

    

    


if __name__ == "__main__":
    main()
