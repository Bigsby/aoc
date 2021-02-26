#! /usr/bin/python3
import sys, os, time
from typing import Dict, Iterable, List, Tuple
import re
from functools import reduce
from math import sqrt

Tile = List[complex]


def getSize(tile: Tile, height: bool = False) -> int:
    if height:
        return int(max(map(lambda value: value.imag, tile)))
    return int(max(map(lambda value: value.real, tile)))


def printTile(tile: Tile):
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


def mirrorHorizontal(tile: Tile, size: int) -> Tile:
    return [ position.imag * 1j + size - position.real for position in tile ]


def rotateClockwise(tile: Tile, size: int) -> Tile:
    return [ position.real * 1j + size - position.imag for position in tile ]


def generatePermutations(tile: Tile) -> Iterable[Tile]:
    size = getSize(tile)
    for _ in range(4):
        yield tile
        yield mirrorHorizontal(tile, size)
        tile = rotateClockwise(tile, size)


def generateAllTilesPermutations(tiles: List[Tuple[int,Tile]]) -> Dict[int,List[Tile]]:
    return { number: list(generatePermutations(tile)) for number, tile in tiles }


TESTS = {  # ( startOfTileA, StartOfTileB, StepToNextPosition )
    -1j: ( 0 , 1j, 1  ), # match top with bottom left to right
      1: ( 1 ,  0, 1j ), # match right with left top to bottom
     1j: ( 1j,  0, 1  ), # match bottom with top left to right
     -1: ( 0 ,  1, 1j )  # mathc left with right top to bottom
}
def testSides(tileA: Tile, tileB: Tile, side: complex, size: int) -> bool:
    positionAStart, positionBStart, step = TESTS[side]
    positionA = positionAStart * size
    positionB = positionBStart * size
    for _ in range(size + 1):
        if (positionA in tileA) ^ (positionB in tileB):
            return False
        positionA += step
        positionB += step
    return True


def doPermutationsMatch(permutationA: Tile, permutationB:Tile, size:int, sides: List[complex]) -> Tuple[bool, complex]:
    for side in sides:
        if testSides(permutationA, permutationB, side, size):
            return True, side
    return False, 0
    

def doTilesMatch(tileA: Tile, permutations: List[Tile], size: int, sides: List[complex] = list(TESTS.keys())) -> Tuple[bool,complex, Tile]:
    for permutation in permutations:
        matched, side = doPermutationsMatch(tileA, permutation, size, sides)
        if matched:
            return True, side, permutation
    return False, 0, []


def getMatchingSides(tile: Tuple[int,Tile], tiles:List[Tuple[int,Tile]], size: int, allPermutations: Dict[int,List[Tile]]) -> List[complex]:
    number, thisTile = tile
    matchedSides = []
    for otherNumber, _ in tiles:
        if otherNumber == number:
            continue
        matched, side, _ = doTilesMatch(thisTile, allPermutations[otherNumber], size)
        if matched:
            matchedSides.append(side)
    return matchedSides


def getCorners(tiles: List[Tuple[int,Tile]], size: int, allPermutations: Dict[int,List[Tile]]) -> List[Tuple[int,Tile]]:
    tilesMatchesSides = { number: getMatchingSides((number, tile), tiles, size, allPermutations) for number, tile in tiles }
    return [ ( number, matchedSides ) for number, matchedSides in tilesMatchesSides.items() if len(matchedSides) == 2 ]


def buildPuzzle(tiles: List[Tuple[int,Tile]], tileSize: int, tilePermutations: Dict[int,List[Tile]], corners: List[Tuple[int,Tile]]) -> Dict[complex,Tile]:
    firstCornerNumber, (sideOne, sideTwo) = corners[0]
    puzzleWidth = int(sqrt(len(tiles)))
    puzzlePosition = (puzzleWidth - 1) * ((1 if sideOne == -1 or sideTwo == -1 else 0) + (1j if sideOne == -1j or sideTwo == -1j else 0))
    lastTile = tilePermutations[firstCornerNumber][0]
    del tilePermutations[firstCornerNumber]
    puzzle = { }
    puzzle[puzzlePosition] = lastTile
    direction = sideOne
    while tilePermutations:
        puzzlePosition += direction
        for tileNumber, permutations in tilePermutations.items():
            matched, _, matchedPermutation = doTilesMatch(lastTile, permutations, tileSize, [ direction ])
            if matched:
                puzzle[puzzlePosition] = lastTile = matchedPermutation
                del tilePermutations[tileNumber]
                if direction == sideTwo:
                    direction = (-1 if (len(puzzle) // puzzleWidth) % 2 else 1) * sideOne
                elif len(puzzle) % puzzleWidth == 0:
                    direction = sideTwo    
                break
    return puzzle


def removeBordersAndJoin(puzzle: Dict[complex,Tile], tileSize: int) -> List[complex]:
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
def getSeaMonster() -> Tile:
    seaMonster = []
    for rowIndex, row in enumerate(SEA_MONSTER):
        for columnIndex, c in enumerate(row):
            if c == "#":
                seaMonster.append(columnIndex + rowIndex * 1j)
    return seaMonster


def isMonsterInLocation(location: complex, puzzle: Tile, seaMonster: Tile) -> bool:
    for monsterPosition in seaMonster:
        if not location + monsterPosition in puzzle:
            return False
    return True


def getSeaMonsterCount(puzzle: Tile, seaMonster: Tile) -> int:
    seaMonsterWidth = getSize(seaMonster) + 1
    seaMonsterHeight = getSize(seaMonster, True) + 1
    puzzleSize = getSize(puzzle) + 1
    for permutation in generatePermutations(puzzle):
        count = 0
        for puzzleX in range(0, puzzleSize - seaMonsterWidth):
            for puzzleY in range(0, puzzleSize - seaMonsterHeight):
                if isMonsterInLocation(puzzleX + puzzleY * 1j, permutation, seaMonster):
                    count += 1
        if count:
            return count
    return 0
    

def part2(tiles: List[Tuple[int,Tile]], tilePermutations: Dict[int,List[Tile]], corners: List[Tuple[int,Tile]]) -> int:
    tileSize = getSize(tiles[0][1])
    puzzle = buildPuzzle(tiles, tileSize, tilePermutations, corners)
    reduced = removeBordersAndJoin(puzzle, tileSize)
    seaMonster = getSeaMonster()
    locationCount = getSeaMonsterCount(reduced, seaMonster)
    return len(reduced) - len(seaMonster) * locationCount


def solve(tiles: List[Tuple[int,Tile]]) -> Tuple[int,int]:
    permutations = generateAllTilesPermutations(tiles)
    size = getSize(tiles[0][1])
    corners = getCorners(tiles, size, permutations)
    return (
        reduce(lambda soFar, corner: soFar * corner[0], corners, 1),
        part2(tiles, permutations, corners)
    )


numberLineRegex = re.compile(r"^Tile\s(?P<number>\d+):$")
def getInput(filePath: str) -> List[Tuple[int,Tile]]:
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

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()