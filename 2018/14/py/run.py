#! /usr/bin/python3

import sys
import os
import time
from typing import Tuple


def solve(target: int) -> Tuple[str, int]:
    score_sequence = str(target)
    sequence_length = len(score_sequence)
    recipes = "37"
    elf1 = 0
    elf2 = 1
    part1_result = ""
    while recipes[-sequence_length:] != score_sequence and recipes[-sequence_length - 1:-1] != score_sequence:
        elf1_score = int(recipes[elf1])
        elf2_score = int(recipes[elf2])
        recipes += str(elf1_score + elf2_score)
        elf1 = (elf1 + elf1_score + 1) % len(recipes)
        elf2 = (elf2 + elf2_score + 1) % len(recipes)
        if not part1_result and len(recipes) > target + 10:
            part1_result = recipes[target:target + 10]
    return part1_result, recipes.index(score_sequence)


def get_input(file_path: str) -> int:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return int(file.read().strip())


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
