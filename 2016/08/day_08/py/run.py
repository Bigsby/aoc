#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from enum import Enum
from itertools import product


CHARACTER_WIDTH = 5
SCREEN_WIDTH = 50
SCREEN_HEIGTH = 6
LETTERS: Dict[int,str] = {
    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11110 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5): "A",

    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5): "B",

    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5): "C",

    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5): "D",

    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5): "E",

    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b11100 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b10000 << CHARACTER_WIDTH * 5): "F",

    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10110 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01110 << CHARACTER_WIDTH * 5): "G",

    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b11110 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5): "H",

    (0b01110 << CHARACTER_WIDTH * 0) + \
    (0b00100 << CHARACTER_WIDTH * 1) + \
    (0b00100 << CHARACTER_WIDTH * 2) + \
    (0b00100 << CHARACTER_WIDTH * 3) + \
    (0b00100 << CHARACTER_WIDTH * 4) + \
    (0b01110 << CHARACTER_WIDTH * 5): "I",

    (0b00110 << CHARACTER_WIDTH * 0) + \
    (0b00010 << CHARACTER_WIDTH * 1) + \
    (0b00010 << CHARACTER_WIDTH * 2) + \
    (0b00010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5): "J",

    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10100 << CHARACTER_WIDTH * 1) + \
    (0b11000 << CHARACTER_WIDTH * 2) + \
    (0b10100 << CHARACTER_WIDTH * 3) + \
    (0b10100 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5): "K",

    (0b10000 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b10000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5): "L",

    (0b01100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5): "O",

    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11100 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b10000 << CHARACTER_WIDTH * 5): "P",

    (0b11100 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b11100 << CHARACTER_WIDTH * 3) + \
    (0b10100 << CHARACTER_WIDTH * 4) + \
    (0b10010 << CHARACTER_WIDTH * 5): "R",

    (0b01110 << CHARACTER_WIDTH * 0) + \
    (0b10000 << CHARACTER_WIDTH * 1) + \
    (0b10000 << CHARACTER_WIDTH * 2) + \
    (0b01100 << CHARACTER_WIDTH * 3) + \
    (0b00010 << CHARACTER_WIDTH * 4) + \
    (0b11100 << CHARACTER_WIDTH * 5): "S",

    (0b10010 << CHARACTER_WIDTH * 0) + \
    (0b10010 << CHARACTER_WIDTH * 1) + \
    (0b10010 << CHARACTER_WIDTH * 2) + \
    (0b10010 << CHARACTER_WIDTH * 3) + \
    (0b10010 << CHARACTER_WIDTH * 4) + \
    (0b01100 << CHARACTER_WIDTH * 5): "U",

    (0b10001 << CHARACTER_WIDTH * 0) + \
    (0b10001 << CHARACTER_WIDTH * 1) + \
    (0b01010 << CHARACTER_WIDTH * 2) + \
    (0b00100 << CHARACTER_WIDTH * 3) + \
    (0b00100 << CHARACTER_WIDTH * 4) + \
    (0b00100 << CHARACTER_WIDTH * 5): "Y",

    (0b11110 << CHARACTER_WIDTH * 0) + \
    (0b00010 << CHARACTER_WIDTH * 1) + \
    (0b00100 << CHARACTER_WIDTH * 2) + \
    (0b01000 << CHARACTER_WIDTH * 3) + \
    (0b10000 << CHARACTER_WIDTH * 4) + \
    (0b11110 << CHARACTER_WIDTH * 5): "Z"
}


class InstructionType(Enum):
    Rect = 0
    RotateRow = 1
    RotateColumn = 2

Instruction = Tuple[InstructionType, int, int]

def printScreen(screen: List[complex], width: int, height: int):
    for y in range(height):
        for x in range(width):
            print("#" if x + y * 1j in screen else ".", end="")
        print()
    print()


def runInstructions(instructions: List[Instruction], width: int, height: int) -> List[complex]:
    screen: List[complex] = []
    toAdd: List[complex] = []
    toRemove: List[complex] = []
    for instructionType, a, b in instructions:
        if instructionType == InstructionType.Rect:
            for x, y in product(range(a), range(b)):
                position = x + y * 1j
                if position not in screen:
                    screen.append(position)
        elif instructionType == InstructionType.RotateRow:
            for position in filter(lambda p: p.imag == a, screen):
                toRemove.append(position)
                toAdd.append(((position.real + b) % width) + position.imag * 1j)
        else:
            for position in filter(lambda p: p.real == a, screen):
                toRemove.append(position)
                toAdd.append(position.real + ((position.imag + b) % height) * 1j)
        for position in toRemove:
            screen.remove(position)
        for position in toAdd:
            screen.append(position)
        toAdd.clear()
        toRemove.clear()
    return screen


def part1(instructions: List[Instruction]) -> int:
    screen = runInstructions(instructions, SCREEN_WIDTH, SCREEN_HEIGTH)
    return len(screen)


def getCharacterInScreen(screen: List[complex], index: int, width: int, height: int) -> str:
    screenValue = sum(2**(width - 1 - x) << (y * width) \
        for y, x in product(range(height), range(width)) \
        if (width * index + x) + y * 1j in screen)
    return LETTERS[screenValue]


def part2(instructions: List[Instruction]) -> str:
    screen = runInstructions(instructions, SCREEN_WIDTH, SCREEN_HEIGTH)
    return "".join(map(lambda index: getCharacterInScreen(screen, index, CHARACTER_WIDTH, SCREEN_HEIGTH), range(SCREEN_WIDTH // CHARACTER_WIDTH)))


def parseLine(line: str) -> Instruction:
    if line.startswith("rect"):
        ab = line[5:].split("x")
        return InstructionType.Rect, int(ab[0]), int(ab[1])
    elif line.startswith("rotate row"):
        ya = line[13:].split(" by ")
        return InstructionType.RotateRow, int(ya[0]), int(ya[1])
    else:
        xa = line[16:].split(" by ")
        return InstructionType.RotateColumn, int(xa[0]), int(xa[1])


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()