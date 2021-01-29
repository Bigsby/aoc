#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

HLF, TPL, INC, JMP, JIE, JIO = 0, 1, 2, 3, 4, 5
Instruction = Tuple[int,str,int]


def runProgram(instructions: List[Instruction], registers: Dict[str,int] = {}) -> int:
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


def part1(instructions: List[Instruction]) -> int:
    return runProgram(instructions)


def part2(instructions: List[Instruction]) -> int:
    return runProgram(instructions, { "a": 1 })


def parseLine(line: str) -> Instruction:
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


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line.strip()) for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()