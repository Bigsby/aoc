#! /usr/bin/python3

from common import getInput, InstructionType, Computer


class ValueMaskComputer(Computer):

    def runValueThroughMask(self, value):
        orMask = int(self.mask.replace("X", "0"), 2)
        value = value | orMask
        andMask = int(self.mask.replace("X", "1"), 2)
        return value & andMask


    def runInstruction(self, instruction):
        if instruction.type == InstructionType.Mask:
            self.setMask(instruction.mask)
        else:
            self.setMemory(instruction.location, self.runValueThroughMask(instruction.value))


def main():
    computer = ValueMaskComputer()
    for instruction in getInput():
        computer.runInstruction(instruction)


    result = computer.getMemorySum()
    print("Result:", result)


if __name__ == "__main__":
    main()
