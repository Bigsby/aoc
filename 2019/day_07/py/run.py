#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from enum import Enum
from itertools import permutations


def getValue(memory: List[int], pointer: int, offset: int, mode: int) -> int:
    value = memory[pointer + offset]
    if mode:
        return value
    return memory[value]


class IntCodeState(Enum):
    Halted = 0
    Polling = 1
    Running = 2
    Outputting = 3


HALT = 99
ADD = 1
MUL = 2
INPUT = 3
OUTPUT = 4
JMP_TRUE = 5
JMP_FALSE = 6
LESS_THAN = 7
EQUALS = 8
def runInstruction(memory: List[int], state: IntCodeState, pointer: int, input: List[int]):
    memory = list(memory)
    instruction = memory[pointer]
    opcode, p1mode, p2mode = instruction % 100, (instruction // 100) % 10, (instruction // 1000) % 10
    output = 0
    if state == IntCodeState.Halted:
        return memory, state, pointer, output
    newState = IntCodeState.Running
    if opcode == ADD:
        memory[memory[pointer + 3]] = getValue(memory, pointer, 1, p1mode) + getValue(memory, pointer, 2, p2mode)
        pointer += 4
    elif opcode == MUL:
        memory[memory[pointer + 3]] = getValue(memory, pointer, 1, p1mode) * getValue(memory, pointer, 2, p2mode)
        pointer += 4
    elif opcode == INPUT:
        if input:
            memory[memory[pointer + 1]] = input.pop()
            pointer += 2
        else:
            newState = IntCodeState.Polling
    elif opcode == OUTPUT:
        output = getValue(memory, pointer, 1, p1mode)
        pointer += 2
        newState = IntCodeState.Outputting
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
    elif opcode == HALT:
        newState = IntCodeState.Halted
    else:
        raise Exception(f"Unknown instruction", pointer, instruction)
    return memory, newState, pointer, output


class IntCodeComputer():
    def __init__(self, memory: List[int], input: List[int]):
        self.memory = memory
        self.state = IntCodeState.Running
        self.pointer = 0
        self.input = input
        self.output = 0
    
    def setInput(self, value: int):
        self.input.insert(0, value)
    
    def tick(self):
        self.memory, self.state, self.pointer, newOutput = runInstruction(self.memory, self.state, self.pointer, self.input)
        if self.state == IntCodeState.Outputting:
            self.output = newOutput
    
    def runUntilHalt(self) -> int:
        while self.state != IntCodeState.Halted:
            self.tick()
        return self.output
    
    def __str__(self):
        return f"s {self.state} p {self.pointer} i {self.input} o {self.output}"


def runPhasesPermutation(memory: List[int], phases: Tuple[int, ...]) -> int:
    output = 0
    for phase in phases:
        output = IntCodeComputer(memory, [output, phase]).runUntilHalt()
    return output


def part1(memory: List[int]):
    return max(runPhasesPermutation(memory, phases) for phases in permutations(range(5)))


def runFeedbackPhasesPermutation(memory: List[int], phases: Tuple[int,...]) -> int:
    amplifiers = [ IntCodeComputer(memory, [ phase ]) for phase in phases ]
    amplifiers[0].setInput(0)
    while any(amplifier.state != IntCodeState.Halted for amplifier in amplifiers):
        for index, amplifier in enumerate(amplifiers):
            amplifier.tick()
            if amplifier.state == IntCodeState.Outputting:
                amplifiers[ index + 1 if index < len(amplifiers) - 1 else 0 ].setInput(amplifier.output)

    return amplifiers[-1].output


def part2(memory: List[int]):
    return max(runFeedbackPhasesPermutation(memory, permutation) for permutation in permutations(range(5, 10)))


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().split(",") ]


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