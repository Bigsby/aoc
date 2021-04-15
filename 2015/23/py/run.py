#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

HLF, TPL, INC, JMP, JIE, JIO = 0, 1, 2, 3, 4, 5
Instruction = Tuple[int,str,int]


def run_program(instructions: List[Instruction], registers: Dict[str,int] = {}) -> int:
    registers = { **{ "a": 0, "b": 0 }, **registers }
    pointer = 0
    while pointer < len(instructions):
        mnemonic, register, value = instructions[pointer]
        jump = 1
        if mnemonic == HLF:
            registers[register] //= 2
        elif mnemonic == TPL:
            registers[register] *= 3
        elif mnemonic == INC:
            registers[register] += 1
        elif mnemonic == JMP:
            jump = value
        elif mnemonic == JIE:
            if registers[register] % 2 == 0:
                jump = value
        elif mnemonic == JIO:
            if registers[register] == 1:
                jump = value
        pointer += jump
    return registers["b"]


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    return (
        run_program(instructions),
        run_program(instructions, { "a": 1 })
    )

def parse_line(line: str) -> Instruction:
    if line.startswith("hlf"):
        return HLF, line.split(" ")[1], 0
    elif line.startswith("tpl"):
        return TPL, line.split(" ")[1], 0
    elif line.startswith("inc"):
        return INC, line.split(" ")[1], 0
    elif line.startswith("jmp"):
        return JMP, "", int(line.split(" ")[1])
    elif line.startswith("jie"):
        return JIE, line.split(" ")[1][:-1], int(line.split(" ")[2])
    elif line.startswith("jio"):
        return JIO, line.split(" ")[1][:-1], int(line.split(" ")[2])
    raise Exception("Bad format", line)


def get_input(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parse_line(line.strip()) for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()