#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Optional

Input = List[List[str]]


def get_pairs(instructions: Input) -> List[Tuple[Optional[int], Optional[int]]]:
    pairs: List[Tuple[Optional[int], Optional[int]]] = []
    for index in range(0, len(instructions), 18):
        if instructions[index + 4][2] == "1":
            pairs.append((int(instructions[index + 15][2]), None))
        else:
            pairs.append((None, int(instructions[index + 5][2])))
    return pairs


def get_model_number(pairs: List[Tuple[Optional[int], Optional[int]]], higher: bool) -> str:
    model_number = [0] * 14
    stack: List[Tuple[int, int]] = []
    start_digit = 9 if higher else 1
    for index, (first, second) in enumerate(pairs):
        if first is not None:
            stack.append((index, first))
        elif second is not None:
            pair_index, pair_value = stack.pop()
            diff = pair_value + second
            if higher:
                model_number[pair_index] = min(start_digit, start_digit - diff)
                model_number[index] = min(start_digit, start_digit + diff)
            else:
                model_number[pair_index] = max(start_digit, start_digit - diff)
                model_number[index] = max(start_digit, start_digit + diff)
    return "".join(str(digit) for digit in model_number)


def solve(instructions: Input) -> Tuple[str, str]:
    pairs = get_pairs(instructions)
    return (get_model_number(pairs, True), get_model_number(pairs, False))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        instructions = []
        for line in file.readlines():
            instructions.append(line.strip().split())
        return instructions


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
