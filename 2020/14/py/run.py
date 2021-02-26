#! /usr/bin/python3

import sys, os, time
from typing import Iterable, List, Tuple
import re
from enum import Enum


class InstructionType(Enum):
    Mask = 0
    Memory = 1


maskRegex = re.compile(r"^mask\s=\s(?P<mask>[X01]+)$")
memoryRegex = re.compile(r"^mem\[(?P<location>[\d]+)]\s=\s(?P<value>[\d]+)$")
class Instruction():
    def __init__(self, inputLine: str):
        maskMatch = maskRegex.match(inputLine)
        if maskMatch:
            self.type = InstructionType.Mask
            self.mask = maskMatch.group("mask")
        else:
            memoryMatch = memoryRegex.match(inputLine)
            if memoryMatch:
                self.type = InstructionType.Memory
                self.location = int(memoryMatch.group("location"))
                self.value = int(memoryMatch.group("value"))
            else:
                raise Exception(f"Unrecognized instruction: {inputLine}")


class Computer():
    def __init__(self):
        self.mask = "X" * 36
        self.memory = {}

    def getMemorySum(self) -> int:
        return sum(self.memory.values())

    def runInstruction(self, instruction: Instruction):
        if instruction.type == InstructionType.Mask:
            self.mask = instruction.mask
        else:
            for location in self.getMemoryLocations(instruction.location):
                self.memory[location] = self.getValue(instruction.value)
    
    def getMemoryLocations(self, location: int) -> Iterable[int]:
        yield location
    
    def getValue(self, value: int) -> int:
        return value

    def getOrMask(self):
        return int(self.mask.replace("X", "0"), 2)
    
    def getAndMask(self):
        return int(self.mask.replace("X", "1"), 2)
    

def runComputer(computer: Computer, puzzleInput: List[Instruction]) -> int:
    for instruction in puzzleInput:
        computer.runInstruction(instruction)
    return computer.getMemorySum()


class ValueMaskComputer(Computer):
    def getValue(self, value: int) -> int:
        return value | self.getOrMask() & self.getAndMask()


xRegex = re.compile("X")
class MemoryMaskComputer(Computer):
    def getMemoryLocations(self, location: int) -> Iterable[int]:
        location |= self.getOrMask()
        maskBitOfffset = len(self.mask) - 1
        flipBits = [ *map(lambda match: maskBitOfffset - match.start(), xRegex.finditer(self.mask)) ]
        for case in range(1 << len(flipBits)):
            currentLocation = location
            for index, flipBit in enumerate(flipBits):
                currentLocation &= ~(1 << flipBit)
                newBit = ((1 << index) & case) >> index
                currentLocation |= newBit << flipBit
            yield currentLocation


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    return (
        runComputer(ValueMaskComputer(), instructions),
        runComputer(MemoryMaskComputer(), instructions)
    )


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ Instruction(line) for line in file.readlines() ]


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