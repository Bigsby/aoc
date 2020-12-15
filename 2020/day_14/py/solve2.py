#! /usr/bin/python3

import re
from functools import reduce

from common import getInput, InstructionType, Computer

xRegex = re.compile("X")

class MemoryMaskComputer(Computer):

    def getValue(self, value):
        return value

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


def main():
    computer = MemoryMaskComputer()
    for instruction in getInput():
        computer.runInstruction(instruction)


    result = computer.getMemorySum()
    print("Result:", result)


if __name__ == "__main__":
    main()
