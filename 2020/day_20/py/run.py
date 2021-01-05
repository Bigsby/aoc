#! /usr/bin/python3
import sys, os, time
import re
from functools import reduce
from math import sqrt


def getSize(tile, height = False):
    if height:
        return int(max(map(lambda value: value.imag, tile)))
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
    startX = int(min(map(lambda value: value.imag, tile)))
    endX = int(max(map(lambda value: value.imag, tile)))
    startY = int(min(map(lambda value: value.real, tile)))
    endY = int(max(map(lambda value: value.real, tile)))
    for row in range(startX, endX + 1):
        for column in range(startY, endY + 1):
            position = column + row * 1j
            print("#" if position in tile else ".", end="")
        print()
    print()


TESTS = {
    -1j: ( 0 , 1j, 1 ), # top > bottom
    1: ( 1 , 0, 1j ), # right > left
    1j: ( 1j, 0, 1  ), # bottom > top
    -1: ( 0 , 1, 1j )  # left > right
}


def testSides(tileA, tileB, test, size):
    positionAStart, positionBStart, step = test
    positionA = positionAStart * size
    positionB = positionBStart * size
    for _ in range(size + 1):
        if (positionA in tileA) ^ (positionB in tileB):
            return False
        positionA += step
        positionB += step
    return True


def doPermutationsMatch(permutationA, permutationB, size):
    for side, test in TESTS.items():
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


def getCorners(tiles, size):
    tilesMatchesSides = { number: getMatchingSides((number, tile), tiles, size) for number, tile in tiles }
    return [ ( number, matchedSides ) for number, matchedSides in tilesMatchesSides.items() if len(matchedSides) == 2 ]


def part1(tiles):
    return reduce(lambda soFar, number: soFar * number[0], getCorners(tiles, getSize(tiles[0][1])), 1)


def findTileForSide(tile, permutations, side, size):
    for permutation in permutations:
        if testSides(tile, permutation, TESTS[side], size):
            return True, permutation
    return False, None


def printPuzzleNumbers(puzzle):
    size = getSize(puzzle)
    for row in range(size + 1):
        for column in range(size + 1):
            print(f" {puzzle[column + row * 1j][0]} ", end="")
        print()


def normalizePuzzlePosition(puzzle):
    minX = abs(min(map(lambda value: value.real, puzzle)))
    minY = abs(min(map(lambda value: value.imag, puzzle)))
    return  { (position.real + minX) + (position.imag + minY) * 1j: tile for position, tile in puzzle.items() }


def buildPuzzle(tiles, tileSize):
    firstCornerNumber, (sideOne, sideTwo) = getCorners(tiles, tileSize)[0]
    tilePermutations = { number: list(buildPermutations(tile)) for number, tile in tiles }
    puzzleWidth = int(sqrt(len(tiles)))
    puzzlePosition = ((1 if sideOne == 3 or sideTwo == 3 else 0) + (1j if sideOne == 0 or sideTwo == 0 else 0)) * (puzzleWidth - 1)
    lastTile = tilePermutations[firstCornerNumber][0]
    del tilePermutations[firstCornerNumber]
    puzzle = { }
    puzzle[puzzlePosition] = lastTile
    direction = sideOne
    nextDirection = -direction
    
    while tilePermutations:
        puzzlePosition += direction
        for tileNumber, permutations in tilePermutations.items():
            matched, newPermutation = findTileForSide(lastTile, permutations, direction, tileSize)
            if matched:
                puzzle[puzzlePosition] = lastTile = newPermutation
                del tilePermutations[tileNumber]
                if direction == sideTwo:
                    direction = nextDirection
                    nextDirection = -direction
                elif len(puzzle) % puzzleWidth == 0:
                    direction = sideTwo    
                break
    return normalizePuzzlePosition(puzzle)


def removeBordersAndJoin(puzzle, tileSize):
    offsetFactor = tileSize - 1
    reduced = []
    for puzzlePosition, tile in puzzle.items():
        for position in tile:
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
    return seaMonster


def isMonsterInLocation(location, puzzle, seaMonster):
    for monsterPosition in seaMonster:
        if not location + monsterPosition in puzzle:
            return False
    return True


def getPermutationWithSeamonster(puzzle, seaMonster):
    seaMonsterWidth = getSize(seaMonster) + 1
    seaMonsterHeight = getSize(seaMonster, True) + 1
    startX = int(min(map(lambda value: value.real, puzzle)))
    endX = int(max(map(lambda value: value.real, puzzle))) + 1
    startY = int(min(map(lambda value: value.imag, puzzle)))
    endY = int(max(map(lambda value: value.imag, puzzle))) + 1
    for permutation in buildPermutations(puzzle):
        count = 0
        for puzzleX in range(startX, endX - seaMonsterWidth):
            for puzzleY in range(startY, endY - seaMonsterHeight):
                if isMonsterInLocation(puzzleX + puzzleY * 1j, permutation, seaMonster):
                    count += 1
        if count:
            return count
    return 0
    

def part2(tiles):
    tileSize = getSize(tiles[0][1])
    puzzle = buildPuzzle(tiles, tileSize)
    reduced = removeBordersAndJoin(puzzle, tileSize)
    seaMonster = getSeaMonster()
    locationCount = getPermutationWithSeamonster(reduced, seaMonster)
    return len(reduced) - len(seaMonster) * locationCount


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