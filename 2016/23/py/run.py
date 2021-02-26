#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re, math

Instruction = List[str]


def getValue(param: str, registers: Dict[str,int]) -> int:
    return int(param) if re.match(r"-?\d+", param) else registers[param]


def runInstructions(instructions: List[Instruction], inputs: Dict[str,int] = {}):
    instructions = instructions[:]
    registers = { register: 0 for register in [ "a", "b", "c", "d" ]}
    registers.update(inputs)
    pointer = 0
    while pointer < len(instructions):
        mnemonic, *params = instructions[pointer]
        if mnemonic == "cpy":
            sourceParam, targetParam = params
            if targetParam in registers:
                registers[targetParam] = getValue(sourceParam, registers)
            pointer += 1
        elif mnemonic == "inc":
            registers[params[0]] += 1
            pointer += 1
        elif mnemonic == "dec":
            registers[params[0]] -= 1
            pointer += 1
        elif mnemonic == "jnz":
            register, jump = params
            value = getValue(register, registers)
            offset = getValue(jump, registers)
            if value != 0:
                pointer += offset
            else:
                pointer += 1
        elif mnemonic == "tgl":
            offset = getValue(params[0], registers)
            pointerToChange = pointer + offset
            if 0 <= pointerToChange < len(instructions):
                newMnemonic, *currentParams = instructions[pointerToChange]
                if newMnemonic == "inc":
                    newMnemonic = "dec"
                elif mnemonic == "dec":
                    newMnemonic = "inc"
                elif newMnemonic == "tgl":
                    newMnemonic = "inc"
                elif newMnemonic == "jnz":
                    newMnemonic = "cpy"
                elif newMnemonic == "cpy":
                    newMnemonic = "jnz"
                instructions[pointerToChange] = [ newMnemonic, *currentParams ]
            pointer += 1
    return registers["a"]


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    a = int(instructions[19][1])
    b = int(instructions[20][1])
    return (
        runInstructions(instructions, { "a": 7 }),
        math.factorial(12) + a * b
    )


def parseLine(line: str) -> Instruction:
    mnemonic = line[:3]
    parameters = line[3:].strip()
    return [ mnemonic ] + parameters.split(" ")


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()