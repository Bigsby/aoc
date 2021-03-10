#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from itertools import product
import re

Point = complex
PointPair = Tuple[Point, complex]
PointPairs = List[PointPair]

CHARACTER_WIDTH = 6
CHARACTER_PADDING = 2
CHARACTER_HEIGHT = 10
LETTERS = {
    (0b001100 << CHARACTER_WIDTH * 0) +
    (0b010010 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b111111 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "A",

    (0b111110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b111110 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b111110 << CHARACTER_WIDTH * 9): "B",

    (0b011110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100000 << CHARACTER_WIDTH * 2) +
    (0b100000 << CHARACTER_WIDTH * 3) +
    (0b100000 << CHARACTER_WIDTH * 4) +
    (0b100000 << CHARACTER_WIDTH * 5) +
    (0b100000 << CHARACTER_WIDTH * 6) +
    (0b100000 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b011110 << CHARACTER_WIDTH * 9): "C",

    (0b111110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b111110 << CHARACTER_WIDTH * 9): "D",

    (0b111111 << CHARACTER_WIDTH * 0) +
    (0b100000 << CHARACTER_WIDTH * 1) +
    (0b100000 << CHARACTER_WIDTH * 2) +
    (0b100000 << CHARACTER_WIDTH * 3) +
    (0b111110 << CHARACTER_WIDTH * 4) +
    (0b100000 << CHARACTER_WIDTH * 5) +
    (0b100000 << CHARACTER_WIDTH * 6) +
    (0b100000 << CHARACTER_WIDTH * 7) +
    (0b100000 << CHARACTER_WIDTH * 8) +
    (0b111111 << CHARACTER_WIDTH * 9): "E",

    (0b111111 << CHARACTER_WIDTH * 0) +
    (0b100000 << CHARACTER_WIDTH * 1) +
    (0b100000 << CHARACTER_WIDTH * 2) +
    (0b100000 << CHARACTER_WIDTH * 3) +
    (0b111110 << CHARACTER_WIDTH * 4) +
    (0b100000 << CHARACTER_WIDTH * 5) +
    (0b100000 << CHARACTER_WIDTH * 6) +
    (0b100000 << CHARACTER_WIDTH * 7) +
    (0b100000 << CHARACTER_WIDTH * 8) +
    (0b100000 << CHARACTER_WIDTH * 9): "F",

    (0b011110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100000 << CHARACTER_WIDTH * 2) +
    (0b100000 << CHARACTER_WIDTH * 3) +
    (0b100000 << CHARACTER_WIDTH * 4) +
    (0b100111 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100011 << CHARACTER_WIDTH * 8) +
    (0b011101 << CHARACTER_WIDTH * 9): "G",

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b111111 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "H",

    (0b111000 << CHARACTER_WIDTH * 0) +
    (0b010000 << CHARACTER_WIDTH * 1) +
    (0b010000 << CHARACTER_WIDTH * 2) +
    (0b010000 << CHARACTER_WIDTH * 3) +
    (0b010000 << CHARACTER_WIDTH * 4) +
    (0b010000 << CHARACTER_WIDTH * 5) +
    (0b010000 << CHARACTER_WIDTH * 6) +
    (0b010000 << CHARACTER_WIDTH * 7) +
    (0b010000 << CHARACTER_WIDTH * 8) +
    (0b111000 << CHARACTER_WIDTH * 9): "I",  # Not sure

    (0b000111 << CHARACTER_WIDTH * 0) +
    (0b000010 << CHARACTER_WIDTH * 1) +
    (0b000010 << CHARACTER_WIDTH * 2) +
    (0b000010 << CHARACTER_WIDTH * 3) +
    (0b000010 << CHARACTER_WIDTH * 4) +
    (0b000010 << CHARACTER_WIDTH * 5) +
    (0b000010 << CHARACTER_WIDTH * 6) +
    (0b100010 << CHARACTER_WIDTH * 7) +
    (0b100010 << CHARACTER_WIDTH * 8) +
    (0b011100 << CHARACTER_WIDTH * 9): "J",

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b100010 << CHARACTER_WIDTH * 1) +
    (0b100100 << CHARACTER_WIDTH * 2) +
    (0b101000 << CHARACTER_WIDTH * 3) +
    (0b110000 << CHARACTER_WIDTH * 4) +
    (0b110000 << CHARACTER_WIDTH * 5) +
    (0b101000 << CHARACTER_WIDTH * 6) +
    (0b100100 << CHARACTER_WIDTH * 7) +
    (0b100010 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "K",

    (0b100000 << CHARACTER_WIDTH * 0) +
    (0b100000 << CHARACTER_WIDTH * 1) +
    (0b100000 << CHARACTER_WIDTH * 2) +
    (0b100000 << CHARACTER_WIDTH * 3) +
    (0b100000 << CHARACTER_WIDTH * 4) +
    (0b100000 << CHARACTER_WIDTH * 5) +
    (0b100000 << CHARACTER_WIDTH * 6) +
    (0b100000 << CHARACTER_WIDTH * 7) +
    (0b100000 << CHARACTER_WIDTH * 8) +
    (0b111111 << CHARACTER_WIDTH * 9): "L",

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b110011 << CHARACTER_WIDTH * 1) +
    (0b110011 << CHARACTER_WIDTH * 2) +
    (0b101101 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "M",  # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b110001 << CHARACTER_WIDTH * 1) +
    (0b110001 << CHARACTER_WIDTH * 2) +
    (0b101001 << CHARACTER_WIDTH * 3) +
    (0b101001 << CHARACTER_WIDTH * 4) +
    (0b100101 << CHARACTER_WIDTH * 5) +
    (0b100101 << CHARACTER_WIDTH * 6) +
    (0b100011 << CHARACTER_WIDTH * 7) +
    (0b100011 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "N",

    (0b011110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b011110 << CHARACTER_WIDTH * 9): "O",

    (0b111110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b111110 << CHARACTER_WIDTH * 4) +
    (0b100000 << CHARACTER_WIDTH * 5) +
    (0b100000 << CHARACTER_WIDTH * 6) +
    (0b100000 << CHARACTER_WIDTH * 7) +
    (0b100000 << CHARACTER_WIDTH * 8) +
    (0b100000 << CHARACTER_WIDTH * 9): "P",

    (0b011110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100101 << CHARACTER_WIDTH * 7) +
    (0b100110 << CHARACTER_WIDTH * 8) +
    (0b011001 << CHARACTER_WIDTH * 9): "Q",  # Not sure

    (0b111110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b111110 << CHARACTER_WIDTH * 4) +
    (0b100100 << CHARACTER_WIDTH * 5) +
    (0b100010 << CHARACTER_WIDTH * 6) +
    (0b100010 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "R",

    (0b011110 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100000 << CHARACTER_WIDTH * 2) +
    (0b100000 << CHARACTER_WIDTH * 3) +
    (0b011110 << CHARACTER_WIDTH * 4) +
    (0b000001 << CHARACTER_WIDTH * 5) +
    (0b000001 << CHARACTER_WIDTH * 6) +
    (0b000001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b011110 << CHARACTER_WIDTH * 9): "S",

    (0b111110 << CHARACTER_WIDTH * 0) +
    (0b001000 << CHARACTER_WIDTH * 1) +
    (0b001000 << CHARACTER_WIDTH * 2) +
    (0b001000 << CHARACTER_WIDTH * 3) +
    (0b001000 << CHARACTER_WIDTH * 4) +
    (0b001000 << CHARACTER_WIDTH * 5) +
    (0b001000 << CHARACTER_WIDTH * 6) +
    (0b001000 << CHARACTER_WIDTH * 7) +
    (0b001000 << CHARACTER_WIDTH * 8) +
    (0b001000 << CHARACTER_WIDTH * 9): "T",  # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b100001 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b011110 << CHARACTER_WIDTH * 9): "U",

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b100001 << CHARACTER_WIDTH * 6) +
    (0b010010 << CHARACTER_WIDTH * 7) +
    (0b010010 << CHARACTER_WIDTH * 8) +
    (0b001100 << CHARACTER_WIDTH * 9): "V",  # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b100001 << CHARACTER_WIDTH * 2) +
    (0b100001 << CHARACTER_WIDTH * 3) +
    (0b100001 << CHARACTER_WIDTH * 4) +
    (0b100001 << CHARACTER_WIDTH * 5) +
    (0b101101 << CHARACTER_WIDTH * 6) +
    (0b101101 << CHARACTER_WIDTH * 7) +
    (0b110011 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "W",  # Not sure

    (0b100001 << CHARACTER_WIDTH * 0) +
    (0b100001 << CHARACTER_WIDTH * 1) +
    (0b010010 << CHARACTER_WIDTH * 2) +
    (0b010010 << CHARACTER_WIDTH * 3) +
    (0b001100 << CHARACTER_WIDTH * 4) +
    (0b001100 << CHARACTER_WIDTH * 5) +
    (0b010010 << CHARACTER_WIDTH * 6) +
    (0b010010 << CHARACTER_WIDTH * 7) +
    (0b100001 << CHARACTER_WIDTH * 8) +
    (0b100001 << CHARACTER_WIDTH * 9): "X",

    (0b100010 << CHARACTER_WIDTH * 0) +
    (0b100010 << CHARACTER_WIDTH * 1) +
    (0b010100 << CHARACTER_WIDTH * 2) +
    (0b010100 << CHARACTER_WIDTH * 3) +
    (0b001000 << CHARACTER_WIDTH * 4) +
    (0b001000 << CHARACTER_WIDTH * 5) +
    (0b001000 << CHARACTER_WIDTH * 6) +
    (0b001000 << CHARACTER_WIDTH * 7) +
    (0b001000 << CHARACTER_WIDTH * 8) +
    (0b001000 << CHARACTER_WIDTH * 9): "Y",  # Not sure

    (0b111111 << CHARACTER_WIDTH * 0) +
    (0b000001 << CHARACTER_WIDTH * 1) +
    (0b000001 << CHARACTER_WIDTH * 2) +
    (0b000010 << CHARACTER_WIDTH * 3) +
    (0b000100 << CHARACTER_WIDTH * 4) +
    (0b001000 << CHARACTER_WIDTH * 5) +
    (0b010000 << CHARACTER_WIDTH * 6) +
    (0b100000 << CHARACTER_WIDTH * 7) +
    (0b100000 << CHARACTER_WIDTH * 8) +
    (0b111111 << CHARACTER_WIDTH * 9): "Z"
}


def print_points(point_pairs: List[PointPair]):
    _, minX, maxX, minY, maxY = get_dimensions(point_pairs)
    points = [point[0] for point in point_pairs]
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            point = x + y * 1j
            if point in points:
                print("#", end="")
            else:
                print(".", end="")
        print()


def get_dimensions(points: List[PointPair]) -> Tuple[Tuple[int, int], int, int, int, int]:
    min_x = int(min(map(lambda point: point[0].real, points)))
    max_x = int(max(map(lambda point: point[0].real, points)))
    min_y = int(min(map(lambda point: point[0].imag, points)))
    max_y = int(max(map(lambda point: point[0].imag, points)))
    size = abs(max_x - min_x + 1), abs(max_y - min_y + 1)
    return size, min_x, max_x, min_y, max_y


def get_next_state(points: List[PointPair]) -> List[PointPair]:
    new_state: List[PointPair] = []
    for point, velocity in points:
        new_state.append((point + velocity, velocity))
    return new_state


def get_character(minX: int, minY: int, index: int, charaterWidth: int, points: List[Point]) -> str:
    screenValue = sum(2**(CHARACTER_WIDTH - 1 - x) << (y * CHARACTER_WIDTH)
                      for y, x in product(range(CHARACTER_HEIGHT), range(CHARACTER_WIDTH))
                      if (charaterWidth * index + x + minX) + (y + minY) * 1j in points)
    return LETTERS[screenValue]


def get_message(pointPairs: List[PointPair]) -> Tuple[bool, str]:
    points = [point[0] for point in pointPairs]
    (width, _), min_x, _, min_y, _ = get_dimensions(pointPairs)
    character_width = CHARACTER_WIDTH + CHARACTER_PADDING
    try:
        return True, "".join(map(lambda index:
                                 get_character(min_x, min_y, index, character_width, points), range((width // character_width) + 1)))
    except:
        return False, ""


def solve(point_pairs: List[PointPair]) -> Tuple[str, int]:
    iterations = 0
    while True:
        (_, height), *_ = get_dimensions(point_pairs)
        if height == CHARACTER_HEIGHT:
            success, message = get_message(point_pairs)
            if success:
                return message, iterations
        iterations += 1
        point_pairs = get_next_state(point_pairs)


line_regex = re.compile(
    r"^position=<\s?(?P<positionX>-?\d+),\s+(?P<positionY>-?\d+)>\svelocity=<\s?(?P<velocityX>-?\d+),\s+?(?P<velocityY>-?\d+)>$")


def parse_line(line: str) -> Tuple[complex, complex]:
    match = line_regex.match(line.strip())
    if match:
        return int(match.group("positionX")) + int(match.group("positionY")) * 1j, int(match.group("velocityX")) + int(match.group("velocityY")) * 1j
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[PointPair]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
