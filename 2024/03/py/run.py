#! /usr/bin/python3

import sys, os, time
from typing import Tuple

Input = str

def do_multiplications(puzzle_input: Input, enable_switch: bool) -> int:
    total = 0
    current_index = 0
    enabled = True
    while True:
        next_mul_index = puzzle_input.find("mul", current_index)
        if enable_switch:
            next_do_index = puzzle_input.find("do", current_index)
            if next_do_index != -1 and next_do_index < next_mul_index:
                if puzzle_input[next_do_index + 2:next_do_index + 4] == "()":
                    enabled = True
                    current_index = next_do_index + 4
                    continue
                elif puzzle_input[next_do_index + 2:next_do_index + 7] == "n't()":
                    enabled = False
                    current_index = next_do_index + 6
                    continue
        if next_mul_index == -1:
            break
        current_index = next_mul_index + 3
        if puzzle_input[current_index] != "(":
            continue
        current_index += 1
        number_index = current_index
        while puzzle_input[current_index].isdigit():
            current_index += 1
        if puzzle_input[current_index] != ",":
            continue
        first_value = int(puzzle_input[number_index:current_index])
        current_index += 1
        number_index = current_index 
        while puzzle_input[current_index].isdigit():
            current_index += 1
        if puzzle_input[current_index] != ")":
            continue
        if enabled:
            total += first_value * int(puzzle_input[number_index:current_index])
    return total


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (do_multiplications(puzzle_input, False), do_multiplications(puzzle_input, True))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return file.read().strip()


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
