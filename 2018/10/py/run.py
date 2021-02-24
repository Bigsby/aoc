#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from itertools import product
import re

Point = complex
PointPair = Tuple[Point,complex]
PointPairs = List[PointPair]

CHARACTER_WIDTH = 6
CHARACTER_PADDING = 2
CHARACTER_HEIGHT = 10
LETTERS = {
    (0b001100 << CHARACTER_WIDTH * 0) + \
    (0b010010 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b111111 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "A",

    (0b111110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b111110 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b111110 << CHARACTER_WIDTH * 9): "B",

    (0b011110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100000 << CHARACTER_WIDTH * 2) + \
    (0b100000 << CHARACTER_WIDTH * 3) + \
    (0b100000 << CHARACTER_WIDTH * 4) + \
    (0b100000 << CHARACTER_WIDTH * 5) + \
    (0b100000 << CHARACTER_WIDTH * 6) + \
    (0b100000 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b011110 << CHARACTER_WIDTH * 9): "C",

    (0b111110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b111110 << CHARACTER_WIDTH * 9): "D",

    (0b111111 << CHARACTER_WIDTH * 0) + \
    (0b100000 << CHARACTER_WIDTH * 1) + \
    (0b100000 << CHARACTER_WIDTH * 2) + \
    (0b100000 << CHARACTER_WIDTH * 3) + \
    (0b111110 << CHARACTER_WIDTH * 4) + \
    (0b100000 << CHARACTER_WIDTH * 5) + \
    (0b100000 << CHARACTER_WIDTH * 6) + \
    (0b100000 << CHARACTER_WIDTH * 7) + \
    (0b100000 << CHARACTER_WIDTH * 8) + \
    (0b111111 << CHARACTER_WIDTH * 9): "E",

    (0b111111 << CHARACTER_WIDTH * 0) + \
    (0b100000 << CHARACTER_WIDTH * 1) + \
    (0b100000 << CHARACTER_WIDTH * 2) + \
    (0b100000 << CHARACTER_WIDTH * 3) + \
    (0b111110 << CHARACTER_WIDTH * 4) + \
    (0b100000 << CHARACTER_WIDTH * 5) + \
    (0b100000 << CHARACTER_WIDTH * 6) + \
    (0b100000 << CHARACTER_WIDTH * 7) + \
    (0b100000 << CHARACTER_WIDTH * 8) + \
    (0b100000 << CHARACTER_WIDTH * 9): "F",

    (0b011110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100000 << CHARACTER_WIDTH * 2) + \
    (0b100000 << CHARACTER_WIDTH * 3) + \
    (0b100000 << CHARACTER_WIDTH * 4) + \
    (0b100111 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100011 << CHARACTER_WIDTH * 8) + \
    (0b011101 << CHARACTER_WIDTH * 9): "G",

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b111111 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "H",

    (0b111000 << CHARACTER_WIDTH * 0) + \
    (0b010000 << CHARACTER_WIDTH * 1) + \
    (0b010000 << CHARACTER_WIDTH * 2) + \
    (0b010000 << CHARACTER_WIDTH * 3) + \
    (0b010000 << CHARACTER_WIDTH * 4) + \
    (0b010000 << CHARACTER_WIDTH * 5) + \
    (0b010000 << CHARACTER_WIDTH * 6) + \
    (0b010000 << CHARACTER_WIDTH * 7) + \
    (0b010000 << CHARACTER_WIDTH * 8) + \
    (0b111000 << CHARACTER_WIDTH * 9): "I", # Not sure

    (0b000111 << CHARACTER_WIDTH * 0) + \
    (0b000010 << CHARACTER_WIDTH * 1) + \
    (0b000010 << CHARACTER_WIDTH * 2) + \
    (0b000010 << CHARACTER_WIDTH * 3) + \
    (0b000010 << CHARACTER_WIDTH * 4) + \
    (0b000010 << CHARACTER_WIDTH * 5) + \
    (0b000010 << CHARACTER_WIDTH * 6) + \
    (0b100010 << CHARACTER_WIDTH * 7) + \
    (0b100010 << CHARACTER_WIDTH * 8) + \
    (0b011100 << CHARACTER_WIDTH * 9): "J",

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b100010 << CHARACTER_WIDTH * 1) + \
    (0b100100 << CHARACTER_WIDTH * 2) + \
    (0b101000 << CHARACTER_WIDTH * 3) + \
    (0b110000 << CHARACTER_WIDTH * 4) + \
    (0b110000 << CHARACTER_WIDTH * 5) + \
    (0b101000 << CHARACTER_WIDTH * 6) + \
    (0b100100 << CHARACTER_WIDTH * 7) + \
    (0b100010 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "K",

    (0b100000 << CHARACTER_WIDTH * 0) + \
    (0b100000 << CHARACTER_WIDTH * 1) + \
    (0b100000 << CHARACTER_WIDTH * 2) + \
    (0b100000 << CHARACTER_WIDTH * 3) + \
    (0b100000 << CHARACTER_WIDTH * 4) + \
    (0b100000 << CHARACTER_WIDTH * 5) + \
    (0b100000 << CHARACTER_WIDTH * 6) + \
    (0b100000 << CHARACTER_WIDTH * 7) + \
    (0b100000 << CHARACTER_WIDTH * 8) + \
    (0b111111 << CHARACTER_WIDTH * 9): "L",

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b110011 << CHARACTER_WIDTH * 1) + \
    (0b110011 << CHARACTER_WIDTH * 2) + \
    (0b101101 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "M", # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b110001 << CHARACTER_WIDTH * 1) + \
    (0b110001 << CHARACTER_WIDTH * 2) + \
    (0b101001 << CHARACTER_WIDTH * 3) + \
    (0b101001 << CHARACTER_WIDTH * 4) + \
    (0b100101 << CHARACTER_WIDTH * 5) + \
    (0b100101 << CHARACTER_WIDTH * 6) + \
    (0b100011 << CHARACTER_WIDTH * 7) + \
    (0b100011 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "N",

    (0b011110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b011110 << CHARACTER_WIDTH * 9): "O",

    (0b111110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b111110 << CHARACTER_WIDTH * 4) + \
    (0b100000 << CHARACTER_WIDTH * 5) + \
    (0b100000 << CHARACTER_WIDTH * 6) + \
    (0b100000 << CHARACTER_WIDTH * 7) + \
    (0b100000 << CHARACTER_WIDTH * 8) + \
    (0b100000 << CHARACTER_WIDTH * 9): "P",

    (0b011110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100101 << CHARACTER_WIDTH * 7) + \
    (0b100110 << CHARACTER_WIDTH * 8) + \
    (0b011001 << CHARACTER_WIDTH * 9): "Q", # Not sure

    (0b111110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b111110 << CHARACTER_WIDTH * 4) + \
    (0b100100 << CHARACTER_WIDTH * 5) + \
    (0b100010 << CHARACTER_WIDTH * 6) + \
    (0b100010 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "R",

    (0b011110 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100000 << CHARACTER_WIDTH * 2) + \
    (0b100000 << CHARACTER_WIDTH * 3) + \
    (0b011110 << CHARACTER_WIDTH * 4) + \
    (0b000001 << CHARACTER_WIDTH * 5) + \
    (0b000001 << CHARACTER_WIDTH * 6) + \
    (0b000001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b011110 << CHARACTER_WIDTH * 9): "S",

    (0b111110 << CHARACTER_WIDTH * 0) + \
    (0b001000 << CHARACTER_WIDTH * 1) + \
    (0b001000 << CHARACTER_WIDTH * 2) + \
    (0b001000 << CHARACTER_WIDTH * 3) + \
    (0b001000 << CHARACTER_WIDTH * 4) + \
    (0b001000 << CHARACTER_WIDTH * 5) + \
    (0b001000 << CHARACTER_WIDTH * 6) + \
    (0b001000 << CHARACTER_WIDTH * 7) + \
    (0b001000 << CHARACTER_WIDTH * 8) + \
    (0b001000 << CHARACTER_WIDTH * 9): "T", # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b100001 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b011110 << CHARACTER_WIDTH * 9): "U",

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b100001 << CHARACTER_WIDTH * 6) + \
    (0b010010 << CHARACTER_WIDTH * 7) + \
    (0b010010 << CHARACTER_WIDTH * 8) + \
    (0b001100 << CHARACTER_WIDTH * 9): "V", # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b100001 << CHARACTER_WIDTH * 2) + \
    (0b100001 << CHARACTER_WIDTH * 3) + \
    (0b100001 << CHARACTER_WIDTH * 4) + \
    (0b100001 << CHARACTER_WIDTH * 5) + \
    (0b101101 << CHARACTER_WIDTH * 6) + \
    (0b101101 << CHARACTER_WIDTH * 7) + \
    (0b110011 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "W", # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) + \
    (0b100001 << CHARACTER_WIDTH * 1) + \
    (0b010010 << CHARACTER_WIDTH * 2) + \
    (0b010010 << CHARACTER_WIDTH * 3) + \
    (0b001100 << CHARACTER_WIDTH * 4) + \
    (0b001100 << CHARACTER_WIDTH * 5) + \
    (0b010010 << CHARACTER_WIDTH * 6) + \
    (0b010010 << CHARACTER_WIDTH * 7) + \
    (0b100001 << CHARACTER_WIDTH * 8) + \
    (0b100001 << CHARACTER_WIDTH * 9): "X",

    (0b100010 << CHARACTER_WIDTH * 0) + \
    (0b100010 << CHARACTER_WIDTH * 1) + \
    (0b010100 << CHARACTER_WIDTH * 2) + \
    (0b010100 << CHARACTER_WIDTH * 3) + \
    (0b001000 << CHARACTER_WIDTH * 4) + \
    (0b001000 << CHARACTER_WIDTH * 5) + \
    (0b001000 << CHARACTER_WIDTH * 6) + \
    (0b001000 << CHARACTER_WIDTH * 7) + \
    (0b001000 << CHARACTER_WIDTH * 8) + \
    (0b001000 << CHARACTER_WIDTH * 9): "Y", # Not sure

    (0b111111 << CHARACTER_WIDTH * 0) + \
    (0b000001 << CHARACTER_WIDTH * 1) + \
    (0b000001 << CHARACTER_WIDTH * 2) + \
    (0b000010 << CHARACTER_WIDTH * 3) + \
    (0b000100 << CHARACTER_WIDTH * 4) + \
    (0b001000 << CHARACTER_WIDTH * 5) + \
    (0b010000 << CHARACTER_WIDTH * 6) + \
    (0b100000 << CHARACTER_WIDTH * 7) + \
    (0b100000 << CHARACTER_WIDTH * 8) + \
    (0b111111 << CHARACTER_WIDTH * 9): "Z"
}


def printPoints(pointPairs: List[PointPair]):
    _, minX, maxX, minY, maxY = getDimensions(pointPairs)
    points = [ point[0] for point in pointPairs ]
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            point = x + y * 1j
            if point in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


def getDimensions(points: List[PointPair]) -> Tuple[Tuple[int,int],int,int,int,int]:
    minX = int(min(map(lambda point: point[0].real, points)))
    maxX = int(max(map(lambda point: point[0].real, points)))
    minY = int(min(map(lambda point: point[0].imag, points)))
    maxY = int(max(map(lambda point: point[0].imag, points)))
    size = abs(maxX - minX + 1), abs(maxY - minY + 1)
    return size, minX, maxX, minY, maxY


def getNextState(points: List[PointPair]) -> List[PointPair]:
    result = []
    for position, velocity in points:
        result.append((position + velocity, velocity))
    return result


def getCharacter(minX: int, minY: int, index: int, charaterWidth: int, points: List[Point]) -> str:
    screenValue = sum(2**(CHARACTER_WIDTH - 1 - x) << (y * CHARACTER_WIDTH) \
        for y, x in product(range(CHARACTER_HEIGHT), range(CHARACTER_WIDTH)) \
        if (charaterWidth * index + x + minX) + (y + minY) * 1j in points)
    return LETTERS[screenValue]


def getMessage(pointPairs:List[PointPair]) -> Tuple[bool,str]:
    points = [ point[0] for point in pointPairs ]
    (width, _), minX, _, minY, _ = getDimensions(pointPairs)
    characterWidth = CHARACTER_WIDTH + CHARACTER_PADDING
    try:
        return True, "".join(map(lambda index: getCharacter(minX, minY, index,characterWidth, points),range((width // characterWidth) + 1)))
    except:
        return False, ""


def part1(pointPairs: List[PointPair]) -> Tuple[str,int]:
    iterations = 0
    while True:
        (_, height), *_ = getDimensions(pointPairs)
        if height == CHARACTER_HEIGHT:
            success, message = getMessage(pointPairs)
            if success:
                return message, iterations
        iterations += 1
        pointPairs = getNextState(pointPairs)


lineRegex = re.compile(r"^position=<\s?(?P<positionX>-?\d+),\s+(?P<positionY>-?\d+)>\svelocity=<\s?(?P<velocityX>-?\d+),\s+?(?P<velocityY>-?\d+)>$")
def parseLine(line: str) -> Tuple[complex,complex]:
    match = lineRegex.match(line.strip())
    if match:
        return int(match.group("positionX")) + int(match.group("positionY")) * 1j, int(match.group("velocityX")) + int(match.group("velocityY")) * 1j
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[PointPair]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result, part2Result = part1(puzzleInput)
    middle = time.perf_counter()
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()