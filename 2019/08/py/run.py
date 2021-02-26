#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from itertools import product


IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6
PIXELS_PER_LAYER = IMAGE_WIDTH * IMAGE_HEIGHT
CHARACTER_WIDTH = 5
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


def getImageLayers(pixels: List[int]) -> List[List[int]]:
    layerCount = len(pixels) // PIXELS_PER_LAYER
    return [ pixels[layerIndex * PIXELS_PER_LAYER:PIXELS_PER_LAYER * (layerIndex + 1)] for layerIndex in range(layerCount) ]


def part1(pixels: List[int]) -> int:
    leastZeros = sys.maxsize
    result = 0
    for layer in getImageLayers(pixels):
        zeroCount = layer.count(0)
        if zeroCount < leastZeros:
            leastZeros = zeroCount
            result = layer.count(1) * layer.count(2)
    return result


BLACK = 0
WHITE = 1
TRANSPARENT = 2


def printImage(image: Dict[complex,int]):
    for y, x in product(range(IMAGE_HEIGHT), range(IMAGE_WIDTH)):
        pixel = image[x + y * 1j]
        if pixel == WHITE:
            print("#", end="")
        else:
            print(".", end="")
        if x == IMAGE_WIDTH - 1:
            print()


def getCharacterInImage(image: Dict[complex,int], index: int, width: int, height: int) -> str:
    screenValue = sum(2**(width - 1 - x) << (y * width) \
        for y, x in product(range(height), range(width)) \
        if image[(width * index + x) + y * 1j] == WHITE)
    return LETTERS[screenValue]


def part2(pixels: List[int]) -> str:
    image = { x + y*1j: TRANSPARENT for x, y in product(range(IMAGE_WIDTH), range(IMAGE_HEIGHT)) }
    for layer in getImageLayers(pixels):
        for x, y in product(range(IMAGE_WIDTH), range(IMAGE_HEIGHT)):
            if image[x + y * 1j] < 2:
                continue
            image[x + y * 1j] = layer[x + y * IMAGE_WIDTH]
    return "".join(map(lambda index: getCharacterInImage(image, index, CHARACTER_WIDTH, IMAGE_HEIGHT), range(IMAGE_WIDTH // CHARACTER_WIDTH)))


def solve(pixels: List[int]) -> Tuple[int,str]:
    return (
        part1(pixels),
        part2(pixels)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().strip() ]


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