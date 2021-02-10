#! /usr/bin/python3

import sys, os, time
from typing import Dict, List

Instruction = List[str]

def runInstructions(instructions: List[Instruction], inputs: Dict[str,int] = {}) -> int:
    registers = { register: 0 for register in [ "a", "b", "c", "d" ]}
    registers.update(inputs)
    pointer = 0
    while pointer < len(instructions):
        mnemonic, *params = instructions[pointer]
        if mnemonic == "cpy":
            sourceParam, targetParam = params
            registers[targetParam] = int(sourceParam) if sourceParam.isnumeric() else registers[sourceParam]
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

    return registers["a"]


def part1(instructions: List[Instruction]):
    return runInstructions(instructions)


def part2(instructions: List[Instruction]):
    return runInstructions(instructions, { "c": 1 })


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

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()