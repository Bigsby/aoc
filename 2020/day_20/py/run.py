#! /usr/bin/python3

import sys, os, time
import re
from functools import reduce
from math import sqrt


def mirrorHorizontal(grid):
    size = len(grid)
    return [ [ grid[y][size - 1 - x] for x in range(size) ] for y in range(size) ]


def rotateClockwise(grid):
    size = len(grid)
    return [ [ grid[size - 1 - x][y] for x in range(size) ] for y in range(size) ]


def buildPermutations(lines):
    grid = [list(line) for line in lines]
    for _ in range(4):
        yield grid
        yield mirrorHorizontal(grid)
        grid = rotateClockwise(grid)


def toString(variation):
    return "\n".join(["".join(line) for line in variation])


def calculatBorders(lines):
    width = len(lines[0])
    top = lines[0]
    right = "".join(map(lambda line: line[width - 1], lines))
    bottom = lines[width - 1]
    left = "".join(map(lambda line: line[0], lines))
    return top, right, bottom, left
     

class Tile():
    def __init__(self, number, lines):
        self.number = number
        self.lines = lines
        self.borders = calculatBorders(self.lines)
        self.permutations = list(buildPermutations(self.lines))

    def __str__(self):
        return f"{self.number} {self.borders}"
    def __repr__(self):
        return self.__str__()


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


def part1(tiles):
    tileCounts = {}
    
    for tile in tiles:
        tileCounts[tile.number] = findMatchingBorders(tile, tiles)

    corners = [ tileNumber for tileNumber in tileCounts if tileCounts[tileNumber] == 2 ]
    return reduce(lambda soFar, tileNumber: soFar * tileNumber, corners)


def getSide(permutation, side, size):
    result = []
    width = size - 1
    for i in range(size):
        if side == 0:
            result.append(permutation[0][i])
        elif side == 1:
            result.append(permutation[i][width])
        elif side == 2:
            result.append(permutation[width][i])
        else:
            result.append(permutation[i][0])
    return result


def getOtherSide(side):
    if side == 0:
        return 2
    if side == 1:
        return 3
    if side == 2:
        return 0
    if side == 3:
        return 1


def findConnection(currentPermutation, newTile, direction, size):
    sideToMatch = getSide(currentPermutation, direction, size)
    otherSide = getOtherSide(direction)
    for permutation in newTile.permutations:
        permutationSide = getSide(permutation, otherSide, size)
        if all(sideToMatch[i] == permutationSide[i] for i in range(size)):
            return True, permutation
    return False, None


def buildPuzzle(tiles, startTile, firstDirection, secondDirection, tileSize, puzzleWidth):
    lastTile = (startTile.number, startTile.permutations[0])
    currentRow = [lastTile]
    puzzle = [currentRow]
    used = { startTile.number }
    direction = firstDirection
    nextDirection = getOtherSide(firstDirection)

    while len(used) < len(tiles):
        _, lastPermutation = lastTile
        for tile in tiles:
            if tile.number in used:
                continue
            matched, newPermutation = findConnection(lastPermutation, tile, direction, tileSize)
            if matched:
                lastTile = (tile.number, newPermutation)
                currentRow.insert(0 if direction == 0 or direction == 3 else len(currentRow), lastTile)
                used.add(tile.number)
                if direction == secondDirection:
                    direction = nextDirection
                    nextDirection = getOtherSide(direction)
                elif (len(used) % puzzleWidth) == 0 and len(used) < len(tiles):
                    currentRow = []
                    puzzle.insert(0 if secondDirection == 0 or secondDirection == 3 else len(puzzle), currentRow)
                    direction = secondDirection
                break

    return puzzle


def findMatchingSide(thisSides, otherSides):
    for thisIndex, side in enumerate(thisSides):
        for otherSide in otherSides:
            if side == otherSide or side == otherSide[::-1]:
                return True, thisIndex
    return False, 0


def isCorner(tile, tiles):
    connections = []
    for otherTile in tiles:
        if otherTile.number == tile.number:
            continue
        matched, thisSide = findMatchingSide(tile.borders, otherTile.borders)
        if matched:
            connections.append(thisSide)
    return len(connections) == 2, connections


def findCorner(tiles):
    for tile in tiles:
        isTileCorner, connections = isCorner(tile, tiles)
        if isTileCorner:
            return tile, connections 

def joinPuzzle(puzzle, tileSize, puzzleWidth):
    rows = []
    for tileRow in puzzle:
        for y in range(1, tileSize - 1):
            currentRow = []
            for x in range(puzzleWidth):
                currentRow += tileRow[x][1][y][1:-1]
            rows.append(currentRow)
    return rows


def isMonsterInLocation(x, y, permutation, seaMonster, seaMonsterWidth, seaMonsterHeight):
    for monsterY in range(seaMonsterHeight):
        for monsterX in range(seaMonsterWidth):
            if seaMonster[monsterY][monsterX] == "#" and permutation[y + monsterY][x + monsterX] == ".":
                return False
    return True


def findSeaMonster(permutation, seaMonster, tileSize, seaMonsterWidth, seaMonsterHeight):
    locations = []
    for x in range(0, tileSize - seaMonsterWidth):
        for y in range(0, tileSize - seaMonsterHeight):
            if isMonsterInLocation(x, y, permutation, seaMonster, seaMonsterWidth, seaMonsterHeight):
                locations.append((x, y))
            
    return locations


def getPermutationWithSeaMonster(puzzle, seaMonsterGrid, puzzleSize, seaMonsterWidth, seaMonsterHeight):
    for permutation in buildPermutations(puzzle):
        locations = findSeaMonster(permutation, seaMonsterGrid, puzzleSize, seaMonsterWidth, seaMonsterHeight)
        if len(locations):
            return permutation, locations


def replaceSeaMonsterInPuzzle(puzzle, seaMonster, locations, monsterWidth, monsterHeight):
    for location in locations:
        x, y = location
        for monsterX in range(monsterWidth):
            for monsterY in range(monsterHeight):
                if seaMonster[monsterY][monsterX] == "#":
                    puzzle[y + monsterY][x + monsterX] = "O"


seaMonsterText = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]
def part2(tiles):
    tileSize = len(tiles[0].lines[0])
    puzzleWidth = int(sqrt(len(tiles)))
    firstCorner, connections = findCorner(tiles)
    puzzle = buildPuzzle(tiles, firstCorner, connections[0], connections[1], tileSize, puzzleWidth)
    jointPuzzle = joinPuzzle(puzzle, tileSize, puzzleWidth)
    jointPuzzleSize = len(jointPuzzle)
    seaMonsterGrid = [ list(line) for line in seaMonsterText ]
    seaMonsterWidth = len(seaMonsterGrid[0])
    seaMonsterHeight = len(seaMonsterGrid)
    permutation, locations = getPermutationWithSeaMonster(jointPuzzle, seaMonsterGrid, jointPuzzleSize, seaMonsterWidth, seaMonsterHeight)
    
    replaceSeaMonsterInPuzzle(permutation, seaMonsterGrid, locations, seaMonsterWidth, seaMonsterHeight)
    count = 0
    for row in permutation:
        count += row.count("#")
    return count


numberLineRegex = re.compile(r"^Tile\s(?P<number>\d+):$")
def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        tiles = []
        tileNumber = 0
        lines = []
        for line in file.readlines():
            numberMatch = numberLineRegex.match(line)
            if numberMatch:
                tileNumber = int(numberMatch.group("number"))
                lines = []
            elif line.strip() == "":
                tiles.append(Tile(tileNumber, lines))
            else:
                lines.append(line.strip())
        
        return tiles


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