#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
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


def part1(puzzleInput: str):
    lengths = [ int(c) for c in puzzleInput.split(",") ]
    marks = [ i for i in range(MARKS_COUNT) ]
    marks, *_ = runLengths(marks, lengths, 0, 0)
    return marks[0] * marks[1]


SUFFIX = [ 17, 31, 73, 47, 23 ]
def part2(puzzleInput: str):
    lengths = [ ord(c) for c in puzzleInput ]
    lengths.extend(SUFFIX)
    marks = [ i for i in range(MARKS_COUNT) ]
    currentMark = skip = 0
    for _ in range(64):
        marks, currentMark, skip = runLengths(marks, lengths, currentMark, skip)
    denseHash = map(lambda index: 
        reduce(lambda soFar, mark: 
            soFar ^ mark, marks[index * 16:(index + 1) * 16 ]), range(16))
    return "".join(map(lambda knot: f"{knot:02x}", denseHash))


def solve(puzzleInput: str) -> Tuple[int,str]:
    return (
        part1(puzzleInput),
        part2(puzzleInput)
    )


def getInput(filePath: str) -> str:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return file.read().strip()


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