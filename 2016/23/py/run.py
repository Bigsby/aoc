#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re
import math

Instruction = List[str]


def get_value(param: str, registers: Dict[str, int]) -> int:
    return int(param) if re.match(r"-?\d+", param) else registers[param]


def run_instructions(instructions: List[Instruction], inputs: Dict[str, int] = {}):
    instructions = instructions[:]
    registers = {register: 0 for register in ["a", "b", "c", "d"]}
    registers.update(inputs)
    pointer = 0
    while pointer < len(instructions):
        mnemonic, *params = instructions[pointer]
        if mnemonic == "cpy":
            source_param, target_param = params
            registers[target_param] = get_value(source_param, registers)
            pointer += 1
        elif mnemonic == "inc":
            registers[params[0]] += 1
            pointer += 1
        elif mnemonic == "dec":
            registers[params[0]] -= 1
            pointer += 1
        elif mnemonic == "jnz":
            register, jump = params
            if get_value(register, registers) != 0:
                pointer += get_value(jump, registers)
            else:
                pointer += 1
        elif mnemonic == "tgl":
            offset = get_value(params[0], registers)
            pointer_to_change = pointer + offset
            if 0 <= pointer_to_change < len(instructions):
                new_mnemonic, *current_params = instructions[pointer_to_change]
                if new_mnemonic == "inc":
                    new_mnemonic = "dec"
                elif new_mnemonic == "dec":
                    new_mnemonic = "inc"
                elif new_mnemonic == "tgl":
                    new_mnemonic = "inc"
                elif new_mnemonic == "jnz":
                    new_mnemonic = "cpy"
                elif new_mnemonic == "cpy":
                    new_mnemonic = "jnz"
                instructions[pointer_to_change] = [
                    new_mnemonic, *current_params]
            pointer += 1
    return registers["a"]


def solve(instructions: List[Instruction]) -> Tuple[int, int]:
    a = int(instructions[19][1])
    b = int(instructions[20][1])
    return (
        run_instructions(instructions, {"a": 7}),
        math.factorial(12) + a * b
    )


def parse_line(line: str) -> Instruction:
    mnemonic = line[:3]
    parameters = line[3:].strip()
    return [mnemonic] + parameters.split(" ")


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
