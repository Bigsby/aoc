#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
from collections import defaultdict


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


def is_position_in_beam(memory: List[int], x: int, y: int) -> int:
    robot = IntCodeComputer(memory)
    robot.inputs.append(x)
    robot.inputs.append(y)
    while not robot.outputing:
        robot.tick()
    return robot.get_output()


def part1(memory: List[int]) -> int:
    points_count = 0
    for y in range(50):
        for x in range(50):
            points_count += is_position_in_beam(memory, x, y)
    return points_count


def part2(memory: List[int]) -> int:
    y = offset = 99
    x = 0
    while True:
        while not is_position_in_beam(memory, x, y):
            x += 1
        top_y = y - offset
        if is_position_in_beam(memory, x, top_y) and is_position_in_beam(memory, x + offset, top_y):
            return x * 10000 + top_y
        y += 1


def solve(memory: List[int]) -> Tuple[int, int]:
    return (
        part1(memory),
        part2(memory)
    )


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
