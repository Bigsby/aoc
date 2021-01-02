#! /usr/bin/python3

import sys, os, time
import re
from enum import Enum


class Computer():
    def __init__(self):
        self.mask = "X" * 36
        self.memory = {}

    def setMask(self, mask):
        self.mask = mask
        
    def setMemory(self, location, value):
        self.memory[str(location)] = value

    def getMemorySum(self):
        return sum([ value for _, value in self.memory.items() ])
    
    def getMemoryLocations(_, location):
        yield location
    
    def getValue(_, value):
        return value

    def runInstruction(self, instruction):
        if instruction.type == InstructionType.Mask:
            self.setMask(instruction.mask)
        else:
            for location in self.getMemoryLocations(instruction.location):
                self.setMemory(location, self.getValue(instruction.value))


class InstructionType(Enum):
    Mask = 0
    Memory = 1


maskRegex = re.compile(r"^mask\s=\s(?P<mask>[X01]+)$")
memoryRegex = re.compile(r"^mem\[(?P<location>[\d]+)]\s=\s(?P<value>[\d]+)$")
class Instruction():
    def __init__(self, inputLine):
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
    
    def __str__(self):
        return f"Mask = {self.mask}" if self.type == InstructionType.Mask else f"mem[{self.location}] = {self.value}"
    def __repr__(self):
        return self.__str__()


def runComputer(computer, puzzleInput):
    for instruction in puzzleInput:
        computer.runInstruction(instruction)
    return computer.getMemorySum()


class ValueMaskComputer(Computer):
    def getValue(self, value):
        orMask = int(self.mask.replace("X", "0"), 2)
        value = value | orMask
        andMask = int(self.mask.replace("X", "1"), 2)
        return value & andMask


def part1(puzzleInput):
    return runComputer(ValueMaskComputer(), puzzleInput)


xRegex = re.compile("X")
class MemoryMaskComputer(Computer):
    def getMemoryLocations(self, location):
        orMask = int(self.mask.replace("X", "0"), 2)
        location = location | orMask
        maskBitOfffset = len(self.mask) - 1
        flipBits = [ *map(lambda match: maskBitOfffset - match.start(), xRegex.finditer(self.mask)) ]
        
        for case in range(1 << len(flipBits)):
            currentLocation = location
            for index, flipBit in enumerate(flipBits):
                currentLocation &= ~(1 << flipBit)
                newBit = ((1 << index) & case) >> index
                currentLocation |= newBit << flipBit
            yield currentLocation


def part2(puzzleInput):
    return runComputer(MemoryMaskComputer(), puzzleInput)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ Instruction(line) for line in file.readlines() ]


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