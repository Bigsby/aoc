#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re

Instruction = Tuple[str, int]
JMP = "jmp"
NOP = "nop"
ACC = "acc"


def run_instruction(op: Instruction, accumulator: int, instruction_pointer: int) -> Tuple[int, int]:
    mnemonic, argument = op
    return accumulator + (argument if mnemonic == ACC else 0), \
        instruction_pointer + (argument if mnemonic == JMP else 1)


def run_boot(boot: List[Instruction]) -> Tuple[bool, int]:
    accumulator = 0
    instruction_pointer = 0
    visited: List[int] = []
    boot_length = len(boot)
    while True:
        visited.append(instruction_pointer)
        accumulator, instruction_pointer = run_instruction(
            boot[instruction_pointer], accumulator, instruction_pointer)
        if instruction_pointer in visited:
            return False, accumulator
        if instruction_pointer == boot_length:
            return True, accumulator


def switch_and_test(index: int, boot: List[Instruction]) -> Tuple[bool, int]:
    boot = list(boot)
    mnemonic, argument = boot[index]
    boot[index] = (NOP if mnemonic == JMP else NOP, argument)
    return run_boot(boot)


def part2(boot: List[Instruction]) -> int:
    for index in range(len(boot)):
        if boot[index][0] == ACC:
            continue
        success, accumulator = switch_and_test(index, boot)
        if success:
            return accumulator
    raise Exception("Valid boot not found")


def solve(boot: List[Instruction]) -> Tuple[int, int]:
    return (
        run_boot(boot)[1],
        part2(boot)
    )


line_regex = re.compile(r"^(nop|acc|jmp)\s\+?(-?\d+)$")


def parse_line(line: str) -> Instruction:
    match = line_regex.match(line)
    if match:
        return match.group(1), int(match.group(2))
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
