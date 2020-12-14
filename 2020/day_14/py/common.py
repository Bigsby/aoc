import sys, os, re
from enum import Enum


maskRegex = re.compile(r"^mask\s=\s(?P<mask>[X01]+)$")
memoryRegex = re.compile(r"^mem\[(?P<location>[\d]+)]\s=\s(?P<value>[\d]+)$")


class Computer():
    def __init__(self):
        self.mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.memory = {}

    def setMask(self, mask):
        self.mask = mask
        
    def setMemory(self, location, value):
        self.memory[str(location)] = value

    def getMemorySum(self):
        soFar = 0
        for key in self.memory.keys():
            soFar += self.memory[key]
        return soFar


class InstructionType(Enum):
    Mask = 0
    Memory = 1

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


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            yield Instruction(line)
