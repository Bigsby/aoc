#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Iterable, List, Tuple
from collections import defaultdict
from itertools import product


CHARACTER_WIDTH = 5
LETTERS: Dict[int, str] = {
    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b11110 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "A",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b11100 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b11100 << CHARACTER_WIDTH * 5): "B",

    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "C",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b11100 << CHARACTER_WIDTH * 5): "D",

    (0b11110 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b11100 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b11110 << CHARACTER_WIDTH * 5): "E",

    (0b11110 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b11100 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b10000 << CHARACTER_WIDTH * 5): "F",

    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b10110 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01110 << CHARACTER_WIDTH * 5): "G",

    (0b10010 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b11110 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "H",

    (0b01110 << CHARACTER_WIDTH * 0) +
    (0b00100 << CHARACTER_WIDTH * 1) +
    (0b00100 << CHARACTER_WIDTH * 2) +
    (0b00100 << CHARACTER_WIDTH * 3) +
    (0b00100 << CHARACTER_WIDTH * 4) +
    (0b01110 << CHARACTER_WIDTH * 5): "I",

    (0b00110 << CHARACTER_WIDTH * 0) +
    (0b00010 << CHARACTER_WIDTH * 1) +
    (0b00010 << CHARACTER_WIDTH * 2) +
    (0b00010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "J",

    (0b10010 << CHARACTER_WIDTH * 0) +
    (0b10100 << CHARACTER_WIDTH * 1) +
    (0b11000 << CHARACTER_WIDTH * 2) +
    (0b10100 << CHARACTER_WIDTH * 3) +
    (0b10100 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "K",

    (0b10000 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b10000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b11110 << CHARACTER_WIDTH * 5): "L",

    (0b01100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "O",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b11100 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b10000 << CHARACTER_WIDTH * 5): "P",

    (0b11100 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b11100 << CHARACTER_WIDTH * 3) +
    (0b10100 << CHARACTER_WIDTH * 4) +
    (0b10010 << CHARACTER_WIDTH * 5): "R",

    (0b01110 << CHARACTER_WIDTH * 0) +
    (0b10000 << CHARACTER_WIDTH * 1) +
    (0b10000 << CHARACTER_WIDTH * 2) +
    (0b01100 << CHARACTER_WIDTH * 3) +
    (0b00010 << CHARACTER_WIDTH * 4) +
    (0b11100 << CHARACTER_WIDTH * 5): "S",

    (0b10010 << CHARACTER_WIDTH * 0) +
    (0b10010 << CHARACTER_WIDTH * 1) +
    (0b10010 << CHARACTER_WIDTH * 2) +
    (0b10010 << CHARACTER_WIDTH * 3) +
    (0b10010 << CHARACTER_WIDTH * 4) +
    (0b01100 << CHARACTER_WIDTH * 5): "U",

    (0b10001 << CHARACTER_WIDTH * 0) +
    (0b10001 << CHARACTER_WIDTH * 1) +
    (0b01010 << CHARACTER_WIDTH * 2) +
    (0b00100 << CHARACTER_WIDTH * 3) +
    (0b00100 << CHARACTER_WIDTH * 4) +
    (0b00100 << CHARACTER_WIDTH * 5): "Y",

    (0b11110 << CHARACTER_WIDTH * 0) +
    (0b00010 << CHARACTER_WIDTH * 1) +
    (0b00100 << CHARACTER_WIDTH * 2) +
    (0b01000 << CHARACTER_WIDTH * 3) +
    (0b10000 << CHARACTER_WIDTH * 4) +
    (0b11110 << CHARACTER_WIDTH * 5): "Z"
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

    def __str__(self):
        return f"s {self.running} p {self.pointer} i {self.inputs} o {self.outputs}"


DIRECTION_CHANGES = {
    0: 1j,
    1: -1j
}


def run_program(memory: List[int], panels: Dict[complex, int]) -> Dict[complex, int]:
    robot = IntCodeComputer(memory)
    position = 0j
    heading = 1j
    waiting_for_color = True
    while robot.running:
        robot.tick()
        if robot.polling:
            robot.inputs.append(panels[position] if position in panels else 0)
        elif robot.outputing:
            if waiting_for_color:
                waiting_for_color = False
                panels[position] = robot.get_output()
            else:
                waiting_for_color = True
                heading *= DIRECTION_CHANGES[robot.get_output()]
                position += heading
    return panels


def get_dimensions(points: Iterable[complex]) -> Tuple[Tuple[int, int], int, int, int, int]:
    min_x = int(min(map(lambda point: point.real, points)))
    max_x = int(max(map(lambda point: point.real, points)))
    min_y = int(min(map(lambda point: point.imag, points)))
    max_y = int(max(map(lambda point: point.imag, points)))
    size = abs(max_x - min_x + 1), abs(max_y - min_y + 1)
    return size, min_x, max_x, min_y, max_y


def print_points(panels: List[complex]):
    _, min_x, max_x, min_y, max_y = get_dimensions(panels)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            point = x + y * 1j
            if point in panels:
                print("#", end="")
            else:
                print(".", end="")
        print()


def get_character_in_screen(screen: List[complex], index: int, width: int, height: int,
                            xOffset: int, y_offset: int) -> str:
    screen_value = sum(2**(width - 1 - x) << (y * width)
                      for y, x in product(range(height), range(width))
                      if (width * index + x + xOffset) + (y + y_offset) * 1j in screen)
    return LETTERS[screen_value]


def part2(memory: List[int]):
    panels = run_program(memory, {0: 1})
    panel_points = [point.real - point.imag *
                   1j for point, value in panels.items() if value]
    (width, height), minX, _, minY, _ = get_dimensions(panel_points)
    return "".join(map(lambda index: get_character_in_screen(panel_points, index, CHARACTER_WIDTH, height, minX, minY), range((width // CHARACTER_WIDTH) + 1)))


def solve(memory: List[int]) -> Tuple[int, str]:
    return (
        len(run_program(memory, {0: 0})),
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
