#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
from collections import defaultdict

Position = complex
DIRECTIONS: Dict[int, Position] = {
    1: -1j,
    2:  1j,
    3: -1,
    4:  1
}


class IntCodeComputer():
    def __init__(self, memory: List[int], inputs: List[int] = []):
        self.memory = defaultdict(int, [(index, value)
                                        for index, value in enumerate(memory)])
        self.pointer = 0
        self.inputs = inputs
        self.outputs: List[int] = []
        self.base = 0
        self.running = True
        self.polling = False
        self.outputing = False

    def set_input(self, value: int):
        self.inputs.insert(0, value)

    def run(self) -> List[int]:
        while self.running:
            self.tick()
        return self.outputs

    def get_parameter(self, offset: int, mode: int) -> int:
        value = self.memory[self.pointer + offset]
        if mode == 0:  # POSITION
            return self.memory[value]
        if mode == 1:  # IMMEDIATE
            return value
        elif mode == 2:  # RELATIVE
            return self.memory[self.base + value]
        raise Exception("Unrecognized parameter mode", mode)

    def get_address(self, offset: int, mode: int) -> int:
        value = self.memory[self.pointer + offset]
        if mode == 0:  # POSITION
            return value
        if mode == 2:  # RELATIVE
            return self.base + value
        raise Exception("Unrecognized address mode", mode)

    def get_output(self) -> int:
        self.outputing = False
        return self.outputs.pop()

    def add_input(self, value: int):
        self.inputs.append(value)

    def tick(self):
        instruction = self.memory[self.pointer]
        opcode, p1_mode, p2_mode, p3_mode = instruction % 100, (
            instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10
        if not self.running:
            return
        if opcode == 1:  # ADD
            self.memory[self.get_address(3, p3_mode)] = self.get_parameter(
                1, p1_mode) + self.get_parameter(2, p2_mode)
            self.pointer += 4
        elif opcode == 2:  # MUL
            self.memory[self.get_address(3, p3_mode)] = self.get_parameter(
                1, p1_mode) * self.get_parameter(2, p2_mode)
            self.pointer += 4
        elif opcode == 3:  # INPUT
            if self.inputs:
                self.polling = False
                self.memory[self.get_address(1, p1_mode)] = self.inputs.pop(0)
                self.pointer += 2
            else:
                self.polling = True
        elif opcode == 4:  # OUTPUT
            self.outputing = True
            self.outputs.append(self.get_parameter(1, p1_mode))
            self.pointer += 2
        elif opcode == 5:  # JMP_TRUE
            if self.get_parameter(1, p1_mode):
                self.pointer = self.get_parameter(2, p2_mode)
            else:
                self.pointer += 3
        elif opcode == 6:  # JMP_FALSE
            if not self.get_parameter(1, p1_mode):
                self.pointer = self.get_parameter(2, p2_mode)
            else:
                self.pointer += 3
        elif opcode == 7:  # LESS_THAN
            self.memory[self.get_address(3, p3_mode)] = 1 if self.get_parameter(
                1, p1_mode) < self.get_parameter(2, p2_mode) else 0
            self.pointer += 4
        elif opcode == 8:  # EQUALS
            self.memory[self.get_address(3, p3_mode)] = 1 if self.get_parameter(
                1, p1_mode) == self.get_parameter(2, p2_mode) else 0
            self.pointer += 4
        elif opcode == 9:  # SET_BASE
            self.base += self.get_parameter(1, p1_mode)
            self.pointer += 2
        elif opcode == 99:  # HALT
            self.running = False
        else:
            raise Exception(f"Unknown instruction", self.pointer,
                            instruction, opcode, p1_mode, p2_mode, p3_mode)

    def clone(self):
        clone_computer = IntCodeComputer([])
        clone_computer.memory = dict(self.memory)
        clone_computer.pointer = self.pointer
        clone_computer.base = self.base
        return clone_computer


def draw_area(oxygen: List[Position], walls: List[Position], open_spaces: List[Position]):
    all_posiitons = walls + oxygen
    min_x = int(min(map(lambda p: p.real, all_posiitons)))
    max_x = int(max(map(lambda p: p.real, all_posiitons)))
    min_y = int(min(map(lambda p: p.imag, all_posiitons)))
    max_y = int(max(map(lambda p: p.imag, all_posiitons)))
    for y in range(max_y, min_y - 1, - 1):
        for x in range(min_x, max_x + 1):
            position = x + y * 1j
            c = " "
            if position in walls:
                c = "#"
            if position in open_spaces:
                c = "."
            if position in oxygen:
                c = "O"
            print(c, end="")
        print()
    print()


def run_until_oxygen_system(memory: List[int]) -> Tuple[int, Position, List[Position]]:
    start_position = 0j
    open_spaces: List[Position] = []
    oxygen_position = 0j
    queue = [(start_position, [start_position], IntCodeComputer(memory))]
    visited = [start_position]
    steps_to_oxygen_system = 0
    while queue:
        position, path, droid = queue.pop(0)
        for command, direction in DIRECTIONS.items():
            new_position = position + direction
            if new_position not in visited:
                visited.append(new_position)
                new_droid = droid.clone()
                new_droid.inputs.append(command)
                while not new_droid.outputing:
                    new_droid.tick()
                status = new_droid.get_output()
                if status == 2:  # Oxygen system
                    if steps_to_oxygen_system == 0:
                        steps_to_oxygen_system = len(path)
                    oxygen_position = new_position
                elif status == 1:  # Open space
                    open_spaces.append(new_position)
                    while not new_droid.polling:
                        new_droid.tick()
                    new_path = list(path)
                    new_path.append(new_position)
                    queue.append((new_position, new_path, new_droid))
    return steps_to_oxygen_system, oxygen_position, open_spaces


def solve(memory: List[int]) -> Tuple[int, int]:
    steps_to_oxygen_system, oxygen_system_position, open_spaces = run_until_oxygen_system(
        memory)
    filled = [oxygen_system_position]
    minutes = 0
    while open_spaces:
        minutes += 1
        for oxygen in list(filled):
            for direction in DIRECTIONS.values():
                position = oxygen + direction
                if position in open_spaces:
                    filled.append(position)
                    open_spaces.remove(position)
    return steps_to_oxygen_system, minutes


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [int(i) for i in file.read().split(",")]


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
