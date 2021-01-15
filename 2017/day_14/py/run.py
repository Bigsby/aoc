#! /usr/bin/python3

import sys, os, time
from typing import List, Set, Tuple
from functools import reduce


MARKS_COUNT = 256
def runLengths(marks:List[int], lengths: List[int], currentMark: int, skip: int) -> Tuple[List[int],int,int]:
    for length in lengths:
        toReverse = []
        reverseMark = currentMark
        for _ in range(length):
            toReverse.append(marks[reverseMark])
            reverseMark = reverseMark + 1 if reverseMark < MARKS_COUNT - 1 else 0
        reverseMark = currentMark
        for _ in range(length):
            marks[reverseMark] = toReverse.pop()
            reverseMark = reverseMark + 1 if reverseMark < MARKS_COUNT - 1 else 0
        for _ in range(length + skip):
            currentMark = currentMark + 1 if currentMark < MARKS_COUNT - 1 else 0
        skip += 1
    return marks, currentMark, skip


SUFFIX = [ 17, 31, 73, 47, 23 ]
def knothash(key: str) -> str:
    lengths = [ ord(c) for c in key ]
    lengths.extend(SUFFIX)
    marks = [ i for i in range(MARKS_COUNT) ]
    currentMark = skip = 0
    for _ in range(64):
        marks, currentMark, skip = runLengths(marks, lengths, currentMark, skip)
    denseHash = map(lambda index: reduce(lambda soFar, mark: soFar ^ mark, marks[index * 16:(index + 1) * 16 ]), range(16))
    return "".join(map(lambda knot: f"{knot:02x}", denseHash))


def getRowHashBinaryString(key: str, index: int) -> str:
    rowHash = int(knothash(key + "-" + str(index)), 16)
    return f"{rowHash:0128b}"


def part1(key: str) -> int:
    return sum(map(lambda index: getRowHashBinaryString(key, index).count("1"), range(128)))


DIRECTIONS = [ 1j, 1, -1j, -1 ]
def findAdjacent(point: complex, grid: Set[complex], visited: Set[complex]):
    for direction in DIRECTIONS:
        adjacent = point + direction
        if adjacent in grid and adjacent not in visited:
            visited.add(adjacent)
            findAdjacent(adjacent, grid, visited)


def part2(key: str) -> int:
    pass
    gridPoints = set()
    for row in range(128):
        for column, c in enumerate(getRowHashBinaryString(key, row)):
            if c == "1":
                gridPoints.add(column + row * 1j)
    
    regions = 0
    while gridPoints:
        regions += 1
        point = gridPoints.pop()
        visited = { point }
        findAdjacent(point, gridPoints, visited)
        gridPoints -= visited

    return regions


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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