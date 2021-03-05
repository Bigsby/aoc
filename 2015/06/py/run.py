#! /usr/bin/python3

import sys
import os
import time
from typing import Callable, Dict, List, Tuple
import re

Instruction = Tuple[int, int, int, int, int]
TURN_ON, TOGGLE, TURN_OFF = 0, 1, 2
ACTIONS = {
    "turn on": TURN_ON,
    "toggle": TOGGLE,
    "turn off": TURN_OFF
}
MATRIX_SIDE = 1000


def run_matrix(instructions: List[Instruction], update_funcs: Dict[int, Callable[[int], int]]) -> int:
    matrix = [0] * (MATRIX_SIDE * MATRIX_SIDE)
    for action, x_start, y_start, x_end, y_end in instructions:
        update_func = update_funcs[action]
        for x in range(x_start, x_end + 1):
            for y in range(y_start, y_end + 1):
                position = x + y * MATRIX_SIDE
                matrix[position] = update_func(matrix[position])
    return sum(matrix)


def solve(instructions: List[Instruction]) -> Tuple[int, int]:
    return (run_matrix(instructions, {
        TURN_ON: lambda _: 1,
        TOGGLE: lambda value: not value,
        TURN_OFF: lambda _: 0
    }), run_matrix(instructions, {
        TURN_ON: lambda value: value + 1,
        TOGGLE: lambda value: value + 2,
        TURN_OFF: lambda value: value - 1 if value > 0 else 0
    }))


instruction_regex = re.compile(
    r"^(toggle|turn off|turn on)\s(\d{1,3}),(\d{1,3})\sthrough\s(\d{1,3}),(\d{1,3})$")
def parse_line(line: str) -> Instruction:
    match = instruction_regex.match(line)
    if match:
        return (
            ACTIONS[match.group(1)], 
            int(match.group(2)), 
            int(match.group(3)), 
            int(match.group(4)), 
            int(match.group(5))
        )
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Instruction]:
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
