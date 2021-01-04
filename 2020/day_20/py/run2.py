#! /usr/bin/python3
import sys, os, time
import re
from functools import reduce
from math import sqrt


def getSize(tile):
    return int(max(map(lambda value: value.real, tile)))


def mirrorHorizontal(tile, size):
    return [ position.imag * 1j + size - position.real for position in tile ]


def rotateClockwise(tile, size):
    return [ position.real * 1j + size - position.imag for position in tile ]


def buildPermutations(tile):
    size = getSize(tile)
    for _ in range(4):
        yield tile
        yield mirrorHorizontal(tile, size)
        tile = rotateClockwise(tile, size)
    

def printTile(tile):
    side = getSize(tile) + 1
    for row in range(side):
        for column in range(side):
            position = column + row * 1j
            print("#" if position in tile else ".", end="")
        print()
    print()


TESTS = [
    ( 0 , 1j, 1 ), # top > bottom
    ( 1 , 0, 1j ), # right > left
    ( 1j, 0, 1  ), # bottom > top
    ( 0 , 1, 1j )  # left > right
]
def testSides(tileA, tileB, test, size):
    positionAStart, positionBStart, step = test
    positionA = positionAStart * size
    positionB = positionBStart * size
    for _ in range(size + 1):
        if not (((positionA in tileA) and (positionB in tileB)) or ((positionA not in tileA) and (positionB not in tileB))):
            return False
        positionA += step
        positionB += step
    return True


def doPermutationsMatch(permutationA, permutationB, size):
    for side, test in enumerate(TESTS):
        if testSides(permutationA, permutationB, test, size):
            return True, side
    return False, -1
    

def doTilesMatch(tileA, tileB, size):
    for permutation in buildPermutations(tileB):
        matched, side = doPermutationsMatch(tileA, permutation, size)
        if matched:
            return True, side
    return False, -1


def getMatchingSides(tile, tiles, size):
    number, tile = tile
    matchedSides = []
    for otherNumber, otherTile in tiles:
        if otherNumber == number:
            continue
        matched, side = doTilesMatch(tile, otherTile, size)
        if matched:
            matchedSides.append(side)
    return matchedSides


def part1(tiles):
    size = getSize(tiles[0][1])
    tilesMatchesSides = { number: getMatchingSides((number, tile), tiles, size) for number, tile in tiles }
    corners = [ number for number, matchedSides in tilesMatchesSides.items() if len(matchedSides) == 2 ]
    return reduce(lambda soFar, number: soFar * number, corners)


def findTileForSide(tile, permutations, side, size):
    _, thisTile = tile
    for permutation in permutations:
        if testSides(thisTile, permutation, TESTS[side], size):
            return True, permutation
    return False, None


def printPuzzleNumbers(puzzle):
    size = getSize(puzzle)
    for row in range(size + 1):
        for column in range(size + 1):
            print(f" {puzzle[column + row * 1j][0]} ", end="")
        print()


def getNextDirection(direction):
    return (direction + 2) % 4


SIDE_DIRECTION = {
    0: -1j, # up
    1: 1,   # right
    2: 1j,  # down
    3: -1   # left
}
def buildPuzzle(tiles, tileSize):
    tilesMatchesSides = { number: getMatchingSides((number, tile), tiles, tileSize) for number, tile in tiles }    
    firstCornerNumber, (sideOne, sideTwo) = next((number, matchedSides) for number, matchedSides in tilesMatchesSides.items() if len(matchedSides) == 2)
    allPermutations = { number: list(buildPermutations(tile)) for number, tile in tiles }
    lastTile = firstCornerNumber, allPermutations[firstCornerNumber][0]
    puzzleWidth = int(sqrt(len(tiles)))
    puzzle = { }
    puzzlePosition = ((1 if sideOne == 3 or sideTwo == 3 else 0) + (1j if sideOne == 0 or sideTwo == 0 else 0)) * (puzzleWidth - 1)
    puzzle[puzzlePosition] = lastTile
    used = { firstCornerNumber }
    direction = sideOne
    nextDirection = getNextDirection(direction)
    puzzlePosition += SIDE_DIRECTION[direction]

    while len(used) < len(tiles):
        for tileNumber, _ in tiles:
            if tileNumber in used:
                continue
            matched, newPermutation = findTileForSide(lastTile, allPermutations[tileNumber], direction, tileSize)
            if matched:
                lastTile = (tileNumber, newPermutation)
                puzzle[puzzlePosition] = lastTile
                used.add(tileNumber)
                if direction == sideTwo:
                    direction = nextDirection
                    nextDirection = getNextDirection(direction)
                elif len(used) % puzzleWidth == 0:
                    direction = sideTwo    
                puzzlePosition += SIDE_DIRECTION[direction]
                break

    return puzzle


def removeBordersAndJoin(puzzle, tileSize):
    offsetFactor = tileSize - 1
    reduced = []
    for puzzlePosition, tile in puzzle.items():
        for position in tile[1]:
            if position.real > 0 and position.real < tileSize and position.imag > 0 and position.imag < tileSize:
                reduced.append((puzzlePosition.real * offsetFactor + position.real - 1) + (puzzlePosition.imag * offsetFactor + position.imag - 1) * 1j)
    return reduced


SEA_MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]
def getSeaMonster():
    seaMonster = []
    for rowIndex, row in enumerate(SEA_MONSTER):
        for columnIndex, c in enumerate(row):
            if c == "#":
                seaMonster.append(columnIndex + rowIndex * 1j)
    return seaMonster, len(SEA_MONSTER), len(SEA_MONSTER[0])


def isMonsterInLocation(location, puzzle, seaMonster):
    for monsterPosition in seaMonster:
        if not location + monsterPosition in puzzle:
            return False
    return True


def getSeamonsterLocations(puzzle, seaMonster, seaMonsterHeight, seaMonsterWidth):
    puzzleSize = getSize(puzzle) + 1
    locations = []
    for puzzleRow in range(0, puzzleSize - seaMonsterHeight):
        for puzzleColumn in range(0, puzzleSize - seaMonsterWidth):
            if isMonsterInLocation(puzzleColumn + puzzleRow * 1j, puzzle, seaMonster):
                locations.append(puzzleColumn + puzzleRow * 1j)
    return locations


def getPermutationWithSeamonster(puzzle, seaMonster, seaMonsterHeight, seaMonsterWidth):
    for permutation in buildPermutations(puzzle):
        locations = getSeamonsterLocations(permutation, seaMonster, seaMonsterHeight, seaMonsterWidth)
        if locations:
            return permutation, locations
    return None, []


def removeSeaMonster(puzzle, seaMonster, locations):
    puzzle = list(puzzle)
    for location in locations:
        for seaMonsterPosition in seaMonster:
            puzzle.remove(location + seaMonsterPosition)
    return puzzle
    

def part2(tiles):
    tileSize = getSize(tiles[0][1])
    puzzle = buildPuzzle(tiles, tileSize)
    reduced = removeBordersAndJoin(puzzle, tileSize)
    seaMonster, seaMonsterHeight, seaMonsterWidth = getSeaMonster()
    permutation, locations = getPermutationWithSeamonster(reduced, seaMonster, seaMonsterHeight, seaMonsterWidth)
    withMonster = removeSeaMonster(permutation, seaMonster, locations)
    return len(withMonster)


numberLineRegex = re.compile(r"^Tile\s(?P<number>\d+):$")
def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        tiles = []
        tileNumber = 0
        tile = []
        position = 0j
        for line in file.readlines():
            numberMatch = numberLineRegex.match(line)
            if numberMatch:
                tileNumber = int(numberMatch.group("number"))
                tile = []
                position = 0j
            elif line.strip() == "":
                tiles.append((tileNumber, tile))
            else:
                for c in line.strip():
                    if c == "#":
                        tile.append(position)
                    position += 1
                position += 1j - position.real
            
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