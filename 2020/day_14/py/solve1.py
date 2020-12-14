#! /usr/bin/python3

from functools import reduce

from common import getInput, InstructionType


class Computer():
    def __init__(self):
        self.mask = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
        self.memory = {}

    def setMask(self, mask):
        self.mask = mask
        

    def runValueThroughMask(self, value):
        orMask = int(self.mask.replace("X", "0"), 2)
        value = value | orMask
        andMask = int(self.mask.replace("X", "1"), 2)
        return value & andMask


    def setMemory(self, location, value):
        self.memory[str(location)] = self.runValueThroughMask(value)


    def getMemorySum(self):
        soFar = 0
        for key in self.memory.keys():
            soFar += self.memory[key]
        return soFar
        

    def runInstruction(self, instruction):
        if instruction.type == InstructionType.Mask:
            self.setMask(instruction.mask)
        else:
            self.setMemory(instruction.location, instruction.value)


def main():
    computer = Computer()
    for instruction in getInput():
        computer.runInstruction(instruction)


    result = computer.getMemorySum()
    print("Result:", result)


if __name__ == "__main__":
    main()
