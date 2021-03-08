#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from itertools import permutations


class IntCodeComputer():
    def __init__(self, memory: List[int], inputs: List[int], index: int):
        self.memory = list(memory)
        self.pointer = 0
        self.inputs = inputs
        self.outputs: List[int] = [ ]
        self.running = True
        self.index = index
    
    def run(self) -> List[int]:
        while self.tick():
            pass
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
    
    def tick(self) -> bool:
        if not self.running:
            return False
        instruction = self.memory[self.pointer]
        opcode, p1_mode, p2_mode = instruction % 100, (instruction // 100) % 10, (instruction // 1000) % 10
        if opcode == 1: # ADD
            self.memory[self.getAddress(3)] = self.getParameter(1, p1_mode) + self.getParameter(2, p2_mode)
            self.pointer += 4
        elif opcode == 2: # MUL
            self.memory[self.getAddress(3)] = self.getParameter(1, p1_mode) * self.getParameter(2, p2_mode)
            self.pointer += 4
        elif opcode == 3: # INPUT
            if self.inputs:
                self.memory[self.getAddress(1)] = self.inputs.pop(0)
                self.pointer += 2
        elif opcode == 4: # OUTPUT
            self.outputs.append(self.getParameter(1, p1_mode))
            self.pointer += 2
        elif opcode == 5: # JMP_TRUE
            if self.getParameter(1, p1_mode):
                self.pointer = self.getParameter(2, p2_mode)
            else:
                self.pointer += 3
        elif opcode == 6: # JMP_FALSE
            if not self.getParameter(1, p1_mode):
                self.pointer = self.getParameter(2, p2_mode)
            else:
                self.pointer += 3
        elif opcode == 7: # LESS_THAN
            self.memory[self.getAddress(3)] = 1 if self.getParameter(1, p1_mode) < self.getParameter(2, p2_mode) else 0
            self.pointer += 4
        elif opcode == 8: # EQUALS
            self.memory[self.getAddress(3)] = 1 if self.getParameter(1, p1_mode) == self.getParameter(2, p2_mode) else 0
            self.pointer += 4
        elif opcode == 99: # HALT
            self.running = False
        else:
            raise Exception(f"Unknown instruction", self.pointer, instruction, opcode, p1_mode, p2_mode)
        return self.running
    
    def __str__(self):
        return f"s {self.running} p {self.pointer} i {self.inputs} o {self.outputs}"


def run_phases_permutation(memory: List[int], phases: Tuple[int, ...]) -> int:
    output = 0
    for phase in phases:
        output = IntCodeComputer(memory, [phase, output], 0).run()[0]
    return output


def run_feedback_phases_permutation(memory: List[int], phases: Tuple[int,...]) -> int:
    amplifiers = [ IntCodeComputer(memory, [ phase ], index) for (index, phase) in enumerate(phases) ]
    amplifiers[0].inputs.append(0)
    for i in range(len(amplifiers)):
        amplifiers[i].outputs = amplifiers[(i + 1) % len(amplifiers)].inputs
    while any(amplifier.running for amplifier in amplifiers):
        for amplifier in amplifiers:
            amplifier.tick()
    return amplifiers[-1].outputs[0]


def solve(memory: List[int]) -> Tuple[int,int]:
    return (
        max(run_phases_permutation(memory, phases) for phases in permutations(range(5))),
        max(run_feedback_phases_permutation(memory, permutation) for permutation in permutations(range(5, 10)))
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ int(i) for i in file.read().split(",") ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()