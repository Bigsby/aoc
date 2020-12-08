#! /usr/bin/python3

from common import getInput


def main():
    ops = list(getInput())
    accumulator = 0
    instructionPointer = 0
    visited = []
    while True:
        if instructionPointer in visited:
            break
        visited.append(instructionPointer)
        op = ops[instructionPointer]

        if op.mnemonic == "jmp":
            instructionPointer = instructionPointer + op.argument
            continue

        if op.mnemonic == "acc":
            accumulator = accumulator + op.argument

        instructionPointer = instructionPointer + 1

    print("Accumulator value:", accumulator)

        


if __name__ == "__main__":
    main()
