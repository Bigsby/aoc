#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict
from itertools import product

Input = Tuple[List[complex],List[Tuple[str,int]]]

CHARACTER_WIDTH = 5
SCREEN_WIDTH = 40
SCREEN_HEIGHT = 6
LETTERS: Dict[int, str] = {
    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b11110 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "A",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b11100 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b11100 << CHARACTER_WIDTH * 5): "B",

    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "C",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b11100 << CHARACTER_WIDTH * 5): "D",

    (0b11110 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b11100 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b11110 << CHARACTER_WIDTH * 5): "E",

    (0b11110 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b11100 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b10000 << CHARACTER_WIDTH * 5): "F",

    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b10110 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01110 << CHARACTER_WIDTH * 5): "G",

    (0b10010 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b11110 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "H",

    (0b01110 << CHARACTER_WIDTH * 0) +
    (0b00100 << CHARACTER_WIDTH * 1) +
    (0b00100 << CHARACTER_WIDTH * 2) +
    (0b00100 << CHARACTER_WIDTH * 3) +
    (0b00100 << CHARACTER_WIDTH * 4) +
    (0b01110 << CHARACTER_WIDTH * 5): "I",

    (0b00110 << CHARACTER_WIDTH * 0) +
    (0b00010 << CHARACTER_WIDTH * 1) +
    (0b00010 << CHARACTER_WIDTH * 2) +
    (0b00010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "J",

    (0b10010 << CHARACTER_WIDTH * 0) +
    (0b10100 << CHARACTER_WIDTH * 1) +
    (0b11000 << CHARACTER_WIDTH * 2) +
    (0b10100 << CHARACTER_WIDTH * 3) +
    (0b10100 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "K",

    (0b10000 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b11110 << CHARACTER_WIDTH * 5): "L",

    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "O",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b11100 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b10000 << CHARACTER_WIDTH * 5): "P",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b11100 << CHARACTER_WIDTH * 3) +
    (0b10100 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "R",

    (0b01110 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b01100 << CHARACTER_WIDTH * 3) +
    (0b00010 << CHARACTER_WIDTH * 4) +
    (0b11100 << CHARACTER_WIDTH * 5): "S",

    (0b10010 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "U",

    (0b10001 << CHARACTER_WIDTH * 0) +
    (0b10001 << CHARACTER_WIDTH * 1) +
    (0b01010 << CHARACTER_WIDTH * 2) +
    (0b00100 << CHARACTER_WIDTH * 3) +
    (0b00100 << CHARACTER_WIDTH * 4) +
    (0b00100 << CHARACTER_WIDTH * 5): "Y",

    (0b11110 << CHARACTER_WIDTH * 0) +
    (0b00010 << CHARACTER_WIDTH * 1) +
    (0b00100 << CHARACTER_WIDTH * 2) +
    (0b01000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b11110 << CHARACTER_WIDTH * 5): "Z"
}


def fold_paper(paper: List[complex], folding: Tuple[str,int]) -> List[complex]:
    direction, coordinate = folding
    include_func = (lambda point: point.real) \
                    if direction == "x" else \
                    (lambda point: point.imag)
    new_point_func = (lambda point: 2 * coordinate - point.real + point.imag * 1j) \
                    if direction == "x" else  \
                    (lambda point: point.real + 1j * (2 * coordinate - point.imag))
    new_paper = []
    for point in paper:
        new_paper.append(point if include_func(point) < coordinate else new_point_func(point))
    return list(set(new_paper))


def get_character_in_paper(paper: List[complex], index: int, width: int, height: int) -> str:
    paper_value = sum(2**(width - 1 - x) << (y * width)
                       for y, x in product(range(height), range(width))
                       if (width * index + x) + y * 1j in paper)
    return LETTERS[paper_value]


def solve(puzzle_input: Input) -> Tuple[int,int]:
    points, foldings = puzzle_input
    part1 = 0
    for folding in foldings:
        points = fold_paper(points, folding)
        if not part1:
            part1 = len(points)
    return (
        part1,
        "".join(map(lambda index:
                    get_character_in_paper(points, index,
                                            CHARACTER_WIDTH, SCREEN_HEIGHT), range(SCREEN_WIDTH // CHARACTER_WIDTH)))
    )


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        points = []
        foldings = []
        folding = False
        for line in file.readlines():
            if line == "\n":
                folding = True
                continue
            if folding:
                relevant = line.split(" ")[2].split("=")
                foldings.append((relevant[0], int(relevant[1].strip())))
            else:
                split = line.split(",")
                points.append(int(split[0]) + int(split[1].strip()) * 1j)
        return [points, foldings]


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
