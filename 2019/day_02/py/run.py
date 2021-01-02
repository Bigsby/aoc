#! /usr/bin/python3

import sys, os, time
from itertools import product


HALT = 99
ADD = 1
MUL = 2
def runProgram(memory, noun, verb):
    memory[1] = noun
    memory[2] = verb
    instructionPointer = 0

    while memory[instructionPointer] != HALT:
        instruction = memory[instructionPointer]
        operand1 = memory[instructionPointer + 1]
        operand2 = memory[instructionPointer + 2]
        output = memory[instructionPointer + 3]

        if instruction == ADD:
            memory[output] = memory[operand1] + memory[operand2]
        elif instruction == MUL:
            memory[output] = memory[operand1] * memory[operand2]
        else:
            raise Exception(f"Unknown instruction at {instructionPointer}: {instruction}")

        instructionPointer += 4
        
    return memory[0]


def part1(memory):
    return runProgram(list(memory), 12, 2)


TARGET_VALUE = 19690720
def part2(memory):
    values = [ i for i in range(100) ]
    for noun, verb in product(values, repeat=2):
        result = runProgram(list(memory), noun, verb)
        if result == TARGET_VALUE:
            return 100 * noun + verb


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ *map(int, file.read().strip().split(",")) ]


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