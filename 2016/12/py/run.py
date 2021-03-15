#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple

Instruction = List[str]


def run_instructions(instructions: List[Instruction], inputs: Dict[str, int] = {}) -> int:
    registers = {register: 0 for register in ["a", "b", "c", "d"]}
    registers.update(inputs)
    pointer = 0
    while pointer < len(instructions):
        mnemonic, *params = instructions[pointer]
        # print(instructions[pointer])
        if mnemonic == "cpy":
            source_param, target_param = params
            registers[target_param] = int(
                source_param) if source_param.isnumeric() else registers[source_param]
            pointer += 1
        elif mnemonic == "inc":
            registers[params[0]] += 1
            pointer += 1
        elif mnemonic == "dec":
            registers[params[0]] -= 1
            pointer += 1
        elif mnemonic == "jnz":
            register, jump = params
            if register.isnumeric() or registers[register]:
                pointer += int(jump)
            else:
                pointer += 1
        # print(pointer, registers); input()
    return registers["a"]


def solve(instructions: List[Instruction]) -> Tuple[int, int]:
    return (
        run_instructions(instructions),
        run_instructions(instructions, {"c": 1})
    )


def parse_line(line: str) -> Instruction:
    return list(map(lambda part: part.strip(), line.split(" ")))


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
