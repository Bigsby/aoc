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
    instructionPointer = instructionPointer + argument if mnemonic == JMP else instructionPointer + 1
    if mnemonic == ACC:
        accumulator = accumulator + argument
    return accumulator, instructionPointer


def runBoot(ops: List[Instruction]) -> Tuple[bool,int]:
    accumulator = 0
    instructionPointer = 0
    visited = []
    bootLength = len(ops)
    while True:
        if instructionPointer in visited:
            return False, accumulator
        if instructionPointer == bootLength:
            return True, accumulator
        visited.append(instructionPointer)
        op = ops[instructionPointer]
        accumulator, instructionPointer = runInstruction(op, accumulator, instructionPointer)


def part1(boot: List[Instruction]) -> int:
    return runBoot(boot)[1]


def switchAndTest(index: int, ops: List[Instruction]) -> Tuple[bool,int]:
    ops = list(ops)
    mnemonic, argumant = ops[index]
    ops[index] = (NOP if mnemonic == JMP else NOP, argumant)
    success, accumulator = runBoot(ops)
    return success, accumulator


def part2(boot: List[Instruction]) -> int:
    ops = boot
    for index in range(len(ops)):
        if ops[index][0] == ACC:
            continue
        success, accumulator = switchAndTest(index, ops)
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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()