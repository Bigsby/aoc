#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

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


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    return (
        runInstructions(instructions), 
        runInstructions(instructions, { "c": 1 })
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