#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict
from enum import Enum


CHARACTER_WIDTH = 5
CHARACTER_HEIGHT = 6
SCREEN_WIDTH = 40
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

class OpCode(Enum):
    Addx = 0
    Noop = 1


Input = List[Tuple[OpCode,int]]

def part1(instructions: Input) -> int:
    cycle = 0
    next_test_cycle = 20
    strengths_sum = 0
    register_x = 1
    for opCode, value in instructions:
        for _ in range(1 if opCode == OpCode.Noop else 2):
            cycle += 1
            if cycle == next_test_cycle:
                strengths_sum += register_x * cycle
                next_test_cycle += SCREEN_WIDTH
        register_x += value
    return strengths_sum


def get_letter_in_crt(crt: List[str], index: int, width: int, height: int) -> str:
    screen_value = sum(2**(width - 1 - x) << (y * width)
                      for y in range(height) for x in range(width)
                      if x < width - 1 and crt[(width * index + x) + y * SCREEN_WIDTH] == "#")
    return LETTERS[screen_value]


def part2(instructions: Input) -> str:
    crt = [ "." ] * SCREEN_WIDTH * 6
    cycle = 0
    register_x = 1
    for opCode, value in instructions:
        for _ in range(1 if opCode == OpCode.Noop else 2):
            cycle += 1
            if register_x <= cycle % SCREEN_WIDTH <= register_x + 2:
                crt[cycle - 1] = "#"
        register_x += value
    return "".join(map(lambda index: get_letter_in_crt(crt, index, CHARACTER_WIDTH, CHARACTER_HEIGHT), range((SCREEN_WIDTH // CHARACTER_WIDTH))))


def solve(puzzle_input: Input) -> Tuple[int,str]:
    return (part1(puzzle_input), part2(puzzle_input))


def process_line(line: str) -> Tuple[OpCode,int]:
    split = line.split(" ")
    return (OpCode.Addx, int(split[1])) if split[0] == "addx" else (OpCode.Noop, 0)


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ process_line(line.strip()) for line in file.readlines() ]


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
