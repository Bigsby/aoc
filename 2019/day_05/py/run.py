#! /usr/bin/python3

import sys, os, time


def getValue(memory, pointer, offset, mode):
    value = memory[pointer + offset]
    if mode:
        return value
    return memory[value]


HALT = 99
ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JMP_TRUE = 5
JMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
def run(memory, input):
    memory = list(memory)
    pointer = 0
    output = 0
    while memory[pointer] != HALT:
        instruction = memory[pointer]
        opcode, p1mode, p2mode = instruction % 100, (instruction // 100) % 10, (instruction // 1000) % 10
        if opcode == ADD:
            memory[memory[pointer + 3]] = getValue(memory, pointer, 1, p1mode) + getValue(memory, pointer, 2, p2mode)
            pointer += 4
        elif opcode == MUL:
            memory[memory[pointer + 3]] = getValue(memory, pointer, 1, p1mode) * getValue(memory, pointer, 2, p2mode)
            pointer += 4
        elif opcode == INPUT:
            memory[memory[pointer + 1]] = input
            pointer += 2
        elif opcode == OUTPUT:
            output = getValue(memory, pointer, 1, p1mode)
            pointer += 2
        elif opcode == JMP_TRUE:
            if getValue(memory, pointer, 1, p1mode):
                pointer = getValue(memory, pointer, 2, p2mode)
            else:
                pointer += 3
        elif opcode == JMP_FALSE:
            if not getValue(memory, pointer, 1, p1mode):
                pointer = getValue(memory, pointer, 2, p2mode)
            else:
                pointer += 3
        elif opcode == LESS_THAN:
            memory[memory[pointer + 3]] = 1 if getValue(memory, pointer, 1, p1mode) < getValue(memory, pointer, 2, p2mode) else 0
            pointer += 4
        elif opcode == EQUALS:
            memory[memory[pointer + 3]] = 1 if getValue(memory, pointer, 1, p1mode) == getValue(memory, pointer, 2, p2mode) else 0
            pointer += 4
        else:
            raise Exception(f"Unknown instruction", pointer, instruction)
    return output


def part1(memory):
    return run(memory, 1)


def part2(memory):
    return run(memory, 5)


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().strip().split(",") ]


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