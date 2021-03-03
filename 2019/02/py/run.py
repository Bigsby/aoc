#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from itertools import product


class IntCodeComputer():
    def __init__(self, memory: List[int]):
        self.memory = list(memory)
        self.pointer = 0
        self.running = True
    
    def run(self) -> int:
        while self.running:
            self.tick()
        return self.memory[0]
    
    def get_parameter(self, offset: int) -> int:
        return self.memory[self.memory[self.pointer + offset]]

    def get_address(self, offset: int) -> int:
        return self.memory[self.pointer + offset]
    
    def tick(self):
        opcode = self.memory[self.pointer]
        if not self.running:
            return
        if opcode == 1: # ADD
            self.memory[self.get_address(3)] = self.get_parameter(1) + self.get_parameter(2)
            self.pointer += 4
        elif opcode == 2: # MUL
            self.memory[self.get_address(3)] = self.get_parameter(1) * self.get_parameter(2)
            self.pointer += 4
        elif opcode == 99: # HALT
            self.running = False
        else:
            raise Exception(f"Unknown instruction", self.pointer, opcode)


def run_program(memory: List[int], noun: int, verb: int) -> int:
    memory[1] = noun
    memory[2] = verb
    return IntCodeComputer(memory).run()    


TARGET_VALUE = 19690720
def part2(memory: List[int]) -> int:
    for noun, verb in product([ i for i in range(100) ], repeat=2):
        if run_program(memory, noun, verb) == TARGET_VALUE:
            return 100 * noun + verb
    raise Exception("Target value not found")

def solve(memory: List[int]) -> Tuple[int,int]:
    return (
        run_program(memory, 12, 2),
        part2(memory)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ *map(int, file.read().strip().split(",")) ]


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