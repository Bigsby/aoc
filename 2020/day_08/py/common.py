import sys, os, re


lineRegex = re.compile(r"^(nop|acc|jmp)\s\+?(-?\d+)$")

class Instruction():
    def __init__(self, mnemonic, argument):
        self.mnemonic = mnemonic
        self.argument = int(argument)
    
    def __str__(self):
        return f"{self.mnemonic} {self.argument}"
    def __repr__(self):
        return self.__str__()


def runInstruction(op, accumulator, instructionPointer):
    instructionPointer = instructionPointer + op.argument if op.mnemonic == "jmp" else instructionPointer + 1
    if op.mnemonic == "acc":
        accumulator = accumulator + op.argument
    return accumulator, instructionPointer


def testBoot(ops):
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
            match = lineRegex.match(line)
            if match:
                yield Instruction(match.group(1), match.group(2))
            else:
                raise Exception("Bad format:", line)
