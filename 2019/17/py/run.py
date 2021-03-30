#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
from collections import defaultdict
from itertools import permutations


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


DIRECTIONS = {"v": 1j, ">": 1, "^": -1j, "<": -1}
Scafolds = List[complex]
Robot = Tuple[complex, complex]
PathStretch = Tuple[int, int]
Path = List[str]


def print_area(scafolds: Scafolds, robot: Robot):
    min_x = int(min(map(lambda p: p.real, scafolds)))
    max_x = int(max(map(lambda p: p.real, scafolds)))
    min_y = int(min(map(lambda p: p.imag, scafolds)))
    max_y = int(max(map(lambda p: p.imag, scafolds)))
    print(min_x, max_x, min_y, max_y)
    print(robot)
    for y in range(min_y, max_y + 1):
        for x in range(min_x, max_x + 1):
            position = x + y * 1j
            c = "."
            if position in scafolds:
                c = "#"
            if position == robot[0]:
                c = [c for c, direction in DIRECTIONS.items() if direction ==
                     robot[1]][0]
            print(c, end="")
        print()
    print()


def get_scafolds_and_robot(ascii_computer: IntCodeComputer) -> Tuple[Scafolds, Robot]:
    position = 0j
    scafolds: List[complex] = []
    robot = (0j, 0j)
    while ascii_computer.running:
        ascii_computer.tick()
        if ascii_computer.outputing:
            code = ascii_computer.get_output()
            if code == 35:  # "#"
                scafolds.append(position)
                position += 1
            elif code == 46:  # "."
                position += 1
            elif code == 10:  # line feed
                position = (position.imag + 1) * 1j
            else:
                robot = (position, DIRECTIONS[chr(code)])
                position += 1
    return scafolds, robot


def part1(scafolds: Scafolds) -> int:
    alignment = 0
    for scafold in scafolds:
        if all(map(lambda direction: scafold + direction in scafolds, DIRECTIONS.values())):
            alignment += int(scafold.real) * int(scafold.imag)
    return alignment


TURNS = [(-1j, "L"), (1j, "R")]


def find_path(scafolds: Scafolds, robot: Robot) -> Path:
    path: Path = []
    current_turn = ""
    turn_found = True
    while turn_found:
        position, direction = robot
        if position + direction not in scafolds:
            turn_found = False
            for turn, code in TURNS:
                if position + direction * turn in scafolds:
                    turn_found = True
                    current_turn = code
                    robot = position, direction * turn
        else:
            current_length = 0
            while position + direction in scafolds:
                position += direction
                current_length += 1
            robot = position, direction
            path.append(current_turn)
            path.append(str(current_length))
    return path


def get_repeats_in_path(path: Path, segment: Path) -> List[Tuple[int, int]]:
    return [(start, start + len(segment))
            for start in range(len(path) - len(segment) + 1)
            if path[start:start + len(segment)] == segment]


def is_permutation_valid(path: Path, permutation: Tuple[Tuple[int, int], ...]) -> bool:
    path = list(path)
    for length, repeat_count in permutation:
        segment = path[:length]
        if len(segment) * 2 - 1 > 20:
            return False
        repeat_indexes = get_repeats_in_path(path, segment)
        if len(repeat_indexes) != repeat_count:
            return False
        repeat_indexes.reverse()
        for start, _ in repeat_indexes:
            for _ in range(length):
                del path[start]
    return not path


def get_routines(path: Path) -> Dict[int, Tuple[Path, List[Tuple[int, int]]]]:
    routines: Dict[int, Tuple[Path, List[Tuple[int, int]]]] = {}
    # possible (length, repeat counts)
    for permutation in permutations([(6, 4), (10, 3), (8, 3), (6, 3)], 3):
        if is_permutation_valid(path, permutation):
            indexes_to_group = [i for i in range(len(path))]
            for c, (length, _) in enumerate(permutation):
                index = min(indexes_to_group)
                segment = path[index:index + length]
                repeat_indexes = get_repeats_in_path(path, segment)
                routines[c + ord("A")] = segment, repeat_indexes
                for start, end in repeat_indexes:
                    for i in range(start, end):
                        indexes_to_group.remove(i)
            break
    return routines


def part2(memory: List[int], scafolds: Scafolds, robot: Robot) -> int:
    ascii_computer = IntCodeComputer(memory)
    ascii_computer.memory[0] = 2
    path = find_path(scafolds, robot)
    routines = get_routines(path)
    main_routine_segments: Dict[int, int] = {}
    inputs: List[str] = []
    for routine, (segements, indexes) in routines.items():
        inputs.append(",".join(segements) + chr(10))
        for index_group in indexes:
            main_routine_segments[index_group[0]] = routine
    inputs.insert(0, ",".join([chr(routine) for _, routine in sorted(
        main_routine_segments.items())]) + chr(10))
    inputs.append("n" + chr(10))
    for input_line in inputs:
        for c in input_line:
            ascii_computer.inputs.append(ord(c))
    return ascii_computer.run().pop()


def solve(memory: List[int]) -> Tuple[int, int]:
    ascii_computer = IntCodeComputer(memory)
    scafolds, robot = get_scafolds_and_robot(ascii_computer)
    return (
        part1(scafolds),
        part2(memory, scafolds, robot)
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
