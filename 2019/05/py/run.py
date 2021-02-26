#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


class IntCodeComputer():
    def __init__(self, memory: List[int], inputs: List[int]):
        self.memory = list(memory)
        self.pointer = 0
        self.inputs = inputs
        self.outputs = [ ]
        self.running = True
    
    def runUntilHalt(self) -> List[int]:
        while self.running:
            self.tick()
        return self.outputs
    
    def getParameter(self, offset: int, mode: int) -> int:
        value = self.memory[self.pointer + offset]
        if mode == 0: # POSITION
            return self.memory[value]
        if mode == 1: # IMMEDIATE
            return value
        raise Exception("Unrecognized parameter mode", mode)

    def getAddress(self, offset: int) -> int:
        return self.memory[self.pointer + offset]
    
    def tick(self):
        instruction = self.memory[self.pointer]
        opcode, p1mode, p2mode = instruction % 100, (instruction // 100) % 10, (instruction // 1000) % 10
        if not self.running:
            return
        if opcode == 1: # ADD
            self.memory[self.getAddress(3)] = self.getParameter(1, p1mode) + self.getParameter(2, p2mode)
            self.pointer += 4
        elif opcode == 2: # MUL
            self.memory[self.getAddress(3)] = self.getParameter(1, p1mode) * self.getParameter(2, p2mode)
            self.pointer += 4
        elif opcode == 3: # INPUT
            if self.inputs:
                self.memory[self.getAddress(1)] = self.inputs.pop(0)
                self.pointer += 2
        elif opcode == 4: # OUTPUT
            self.outputs.append(self.getParameter(1, p1mode))
            self.pointer += 2
        elif opcode == 5: # JMP_TRUE
            if self.getParameter(1, p1mode):
                self.pointer = self.getParameter(2, p2mode)
            else:
                self.pointer += 3
        elif opcode == 6: # JMP_FALSE
            if not self.getParameter(1, p1mode):
                self.pointer = self.getParameter(2, p2mode)
            else:
                self.pointer += 3
        elif opcode == 7: # LESS_THAN
            self.memory[self.getAddress(3)] = 1 if self.getParameter(1, p1mode) < self.getParameter(2, p2mode) else 0
            self.pointer += 4
        elif opcode == 8: # EQUALS
            self.memory[self.getAddress(3)] = 1 if self.getParameter(1, p1mode) == self.getParameter(2, p2mode) else 0
            self.pointer += 4
        elif opcode == 99: # HALT
            self.running = False
        else:
            raise Exception(f"Unknown instruction", self.pointer, instruction, opcode, p1mode, p2mode)
    
    def __str__(self):
        return f"s {self.running} p {self.pointer} i {self.inputs} o {self.outputs}"


def solve(memory: List[int]) -> Tuple[int,int]:
    return (
        IntCodeComputer(memory, [1]).runUntilHalt()[-1],
        IntCodeComputer(memory, [5]).runUntilHalt()[-1]
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().strip().split(",") ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()