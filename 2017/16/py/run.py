#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple

Instruction = Tuple[int, int, int]


def to_ord(programs: str) -> List[int]:
    return [ord(c) for c in programs]


def to_str(programs: List[int]) -> str:
    return "".join([chr(c) for c in programs])


def dance(instructions: List[Instruction], programs: List[int]) -> List[int]:
    for move, a, b in instructions:
        if move == 0:
            programs = programs[-a:] + programs[:-a]
        elif move == 1:
            old_a = programs[a]
            programs[a] = programs[b]
            programs[b] = old_a
        elif move == 2:
            a_index = programs.index(a)
            b_index = programs.index(b)
            old_a = programs[a_index]
            programs[a_index] = programs[b_index]
            programs[b_index] = old_a
    return programs


CYCLES = 10**9


def part2(instructions: List[Instruction]) -> str:
    programs = to_ord("abcdefghijklmnop")
    seen = [list(programs)]
    for cycle in range(CYCLES):
        programs = dance(instructions, programs)
        p = list(programs)
        if p in seen:
            return to_str(list(seen[CYCLES % (cycle + 1)]))
        seen.append(p)
    return to_str(programs)


def solve(instructions: List[Instruction]) -> Tuple[str, str]:
    return (
        to_str(dance(instructions, to_ord("abcdefghijklmnop"))),
        part2(instructions)
    )


def parse_instruction(text: str) -> Instruction:
    if text.startswith("s"):
        return (0, int(text[1:]), 0)
    elif text.startswith("x"):
        a, b = text[1:].split("/")
        return (1, int(a), int(b))
    elif text.startswith("p"):
        a, b = text[1:].split("/")
        return (2, ord(a), ord(b))
    raise Exception("Unknow instruction", text)


def get_input(file_path: str) -> List[Instruction]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_instruction(text) for text in file.read().strip().split(",")]


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
