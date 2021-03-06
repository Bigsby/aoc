#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
from collections import defaultdict
import re
from itertools import combinations


class IntCodeComputer():
    def __init__(self, memory: List[int], inputs: List[int] = [], defaultInput: bool = False, defaultValue: int = -1):
        self.memory = defaultdict(int, [(index, value)
                                        for index, value in enumerate(memory)])
        self.pointer = 0
        self.inputs = inputs
        self.outputs: List[int] = []
        self.base = 0
        self.running = True
        self.polling = False
        self.paused = False
        self.outputing = False
        self.default_input = defaultInput
        self.default_value = defaultValue

    def set_input(self, value: int):
        self.inputs.insert(0, value)

    def run(self) -> List[int]:
        while self.running:
            self.tick()
        return self.outputs

    def run_until_paused(self):
        self.paused = False
        while not self.paused and self.running:
            self.tick()
        return self

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
            elif self.default_input:
                self.memory[self.get_address(1, p1_mode)] = self.default_value
                self.pointer += 2
                self.polling = True
            else:
                self.paused = True
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


def parse_room_output(output: str) -> Tuple[str, List[str], List[str]]:
    stage = 0
    room = ""
    doors: List[str] = []
    items: List[str] = []
    for line in output.split("\n"):
        if stage == 0:
            match = re.match(r"^== (?P<room>.*) ==", line)
            if match:
                room = match.group("room")
                stage = 1
        elif stage == 1:
            if line.startswith("Doors"):
                stage = 2
        elif stage == 2:
            match = re.match(r"- (?P<entry>.*)", line)
            if match:
                doors.append(match.group("entry"))
            else:
                stage = 3
        elif stage == 3:
            if line.startswith("Items"):
                stage = 4
        elif stage == 4:
            match = re.match(r"- (?P<entry>.*)", line)
            if match:
                items.append(match.group("entry"))
            else:
                break
    return room, doors, items


def run_command(droid: IntCodeComputer, command: str) -> str:
    if command != "":
        for c in command + '\n':
            droid.inputs.append(ord(c))
    droid.run_until_paused()
    output = "".join(chr(c) for c in droid.outputs)
    droid.outputs.clear()
    return output


# use to play manually
def manual_scout(memory: List[int]):
    print("Scounting")
    droid = IntCodeComputer(memory)
    command = ""
    while command != "quit" and droid.running:
        output = run_command(droid, command)
        print(parse_room_output(output))
        command = input("$ ")


WAY_INVERSE = {
    "": "",
    "north": "south",
    "south": "north",
    "west": "east",
    "east": "west"
}
FORBIDEN_ITEMS = [
    "molten lava",
    "photons",
    "infinite loop",
    "giant electromagnet",
    "escape pod"
]
PRESSURE_ROOM = "Pressure-Sensitive Floor"
SECURITY_CHECKPOINT = "Security Checkpoint"
TAKE = "take "


def navigate_rooms(droid: IntCodeComputer, command: str, destination: str, pickup_items: bool) -> Tuple[str, List[str], str]:
    visited: List[Tuple[str, str]] = []
    way_in: Dict[str, str] = {}
    last_direction = ""
    pressure_room_way_in = ""
    inventory: List[str] = []
    security_doors: List[str] = []
    while droid.running:
        output = run_command(droid, command)
        room, doors, items = parse_room_output(output)
        if room == destination:
            break
        if room == PRESSURE_ROOM:
            pressure_room_way_in = last_direction
            room = SECURITY_CHECKPOINT
            doors = security_doors
        if room == SECURITY_CHECKPOINT:
            security_doors = doors
        if room not in way_in:
            way_in[room] = last_direction
        if pickup_items:
            for item in items:
                if item not in FORBIDEN_ITEMS:
                    run_command(droid, TAKE + item)
                    inventory.append(item)
        new_door = False
        for door in doors:
            if (room, door) not in visited:
                if door == WAY_INVERSE[way_in[room]]:
                    continue
                new_door = True
                visited.append((room, door))
                command = last_direction = door
                break
        if not new_door:
            if way_in[room] == "":
                # in first room
                command = doors[0]
                break
            command = WAY_INVERSE[way_in[room]]
    return command, inventory, pressure_room_way_in


DROP = "drop "


def find_password(memory: List[int]) -> str:
    droid = IntCodeComputer(memory)
    # navigate all rooms and pickup non-forbiden items
    command, inventory, pressure_room_way_in = navigate_rooms(droid, "", "", True)
    # go to Security Checkpoint
    navigate_rooms(droid, command, SECURITY_CHECKPOINT, False)
    # test combinations of items
    for new_inventory in combinations(inventory, 4):
        for item in new_inventory:
            if item not in inventory:
                run_command(droid, TAKE + item)
        for item in inventory:
            if item not in new_inventory:
                run_command(droid, DROP + item)
        output = run_command(droid, pressure_room_way_in)
        password_match = re.search(r"typing (?P<password>\d+)", output)
        if password_match:
            return password_match.group("password")
        inventory = new_inventory
    raise Exception("Password not found")


def solve(memory: List[int]) -> Tuple[str, str]:
    return find_password(memory), ""


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
