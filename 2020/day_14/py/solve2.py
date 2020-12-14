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
        flipBits = []
        locationMask = f"{location:036b}"
        
        for match in xRegex.finditer(self.mask):
            flipBits.append(match.start())

        for case in range(2**len(flipBits)):
            currentLocation = list(locationMask)
            for index, flipBit in enumerate(flipBits):
                newBit = ((2**index) & case) >> index
                currentLocation[flipBit] = str(newBit)
            yield int("".join(currentLocation), 2)



def main():
    computer = MemoryMaskComputer()
    for instruction in getInput():
        computer.runInstruction(instruction)


    result = computer.getMemorySum()
    print("Result:", result)


if __name__ == "__main__":
    main()
