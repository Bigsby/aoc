#! /usr/bin/python3

import sys, os, time
from typing import List
from itertools import product


class IntCodeComputer():
    def __init__(self, memory: List[int]):
        self.memory = list(memory)
        self.pointer = 0
        self.running = True
    
    def runUntilHalt(self) -> int:
        while self.running:
            self.tick()
        return self.memory[0]
    
    def getParameter(self, offset: int) -> int:
        return self.memory[self.memory[self.pointer + offset]]

    def getAddress(self, offset: int) -> int:
        return self.memory[self.pointer + offset]
    
    def tick(self):
        opcode = self.memory[self.pointer]
        if not self.running:
            return
        if opcode == 1: # ADD
            self.memory[self.getAddress(3)] = self.getParameter(1) + self.getParameter(2)
            self.pointer += 4
        elif opcode == 2: # MUL
            self.memory[self.getAddress(3)] = self.getParameter(1) * self.getParameter(2)
            self.pointer += 4
        elif opcode == 99: # HALT
            self.running = False
        else:
            raise Exception(f"Unknown instruction", self.pointer, opcode)


def runProgram(memory: List[int], noun: int, verb: int) -> int:
    memory[1] = noun
    memory[2] = verb
    return IntCodeComputer(memory).runUntilHalt()    


def part1(memory: List[int]) -> int:
    return runProgram(memory, 12, 2)


TARGET_VALUE = 19690720
def part2(memory: List[int]) -> int:
    for noun, verb in product([ i for i in range(100) ], repeat=2):
        if runProgram(memory, noun, verb) == TARGET_VALUE:
            return 100 * noun + verb
    raise Exception("Target value not found")


def getInput(filePath: str) -> List[int]:
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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()