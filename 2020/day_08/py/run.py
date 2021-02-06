#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Instruction = Tuple[str,int]
JMP = "jmp"
NOP = "nop"
ACC = "acc"


def runInstruction(op: Instruction, accumulator: int, instructionPointer: int) -> Tuple[int,int]:
    mnemonic, argument = op
    instructionPointer += argument if mnemonic == JMP else 1
    if mnemonic == ACC:
        accumulator += argument
    return accumulator, instructionPointer


def runBoot(boot: List[Instruction]) -> Tuple[bool,int]:
    accumulator = 0
    instructionPointer = 0
    visited = []
    bootLength = len(boot)
    while True:
        visited.append(instructionPointer)
        accumulator, instructionPointer = runInstruction(boot[instructionPointer], accumulator, instructionPointer)
        if instructionPointer in visited:
            return False, accumulator
        if instructionPointer == bootLength:
            return True, accumulator


def part1(boot: List[Instruction]) -> int:
    return runBoot(boot)[1]


def switchAndTest(index: int, boot: List[Instruction]) -> Tuple[bool,int]:
    boot = list(boot)
    mnemonic, argumant = boot[index]
    boot[index] = (NOP if mnemonic == JMP else NOP, argumant)
    return runBoot(boot)


def part2(boot: List[Instruction]) -> int:
    for index in range(len(boot)):
        if boot[index][0] == ACC:
            continue
        success, accumulator = switchAndTest(index, boot)
        if success:
            return accumulator
    raise Exception("Valid boot not found")


lineRegex = re.compile(r"^(nop|acc|jmp)\s\+?(-?\d+)$")
def parseLine(line: str) -> Instruction:
    match = lineRegex.match(line)
    if match:
        return match.group(1) , int(match.group(2))
    raise Exception("Bad format", line)


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