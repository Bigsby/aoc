#! /usr/bin/python3

import sys, os, time
from typing import Dict, Iterable, List, Tuple
import re
from enum import Enum


class InstructionType(Enum):
    Mask = 0
    Memory = 1


mask_regex = re.compile(r"^mask\s=\s(?P<mask>[X01]+)$")
memory_regex = re.compile(r"^mem\[(?P<location>[\d]+)]\s=\s(?P<value>[\d]+)$")
class Instruction():
    def __init__(self, input_line: str):
        mask_match = mask_regex.match(input_line)
        if mask_match:
            self.type = InstructionType.Mask
            self.mask = mask_match.group("mask")
        else:
            memory_match = memory_regex.match(input_line)
            if memory_match:
                self.type = InstructionType.Memory
                self.location = int(memory_match.group("location"))
                self.value = int(memory_match.group("value"))
            else:
                raise Exception(f"Unrecognized instruction: {input_line}")


class Computer():
    def __init__(self):
        self.mask = "X" * 36
        self.memory: Dict[int, int] = {}

    def get_memory_sum(self) -> int:
        return sum(self.memory.values())

    def run_instruction(self, instruction: Instruction):
        if instruction.type == InstructionType.Mask:
            self.mask = instruction.mask
        else:
            value = self.get_value(instruction.value)
            for location in self.get_memory_locations(instruction.location):
                self.memory[location] = value
    
    def get_memory_locations(self, location: int) -> Iterable[int]:
        yield location
    
    def get_value(self, value: int) -> int:
        return value

    def get_or_mask(self):
        return int(self.mask.replace("X", "0"), 2)
    
    def get_and_mask(self):
        return int(self.mask.replace("X", "1"), 2)
    

def run_computer(computer: Computer, puzzleInput: List[Instruction]) -> int:
    for instruction in puzzleInput:
        computer.run_instruction(instruction)
    return computer.get_memory_sum()


class ValueMaskComputer(Computer):
    def get_value(self, value: int) -> int:
        return (value | self.get_or_mask()) & self.get_and_mask()


xRegex = re.compile("X")
class MemoryMaskComputer(Computer):
    def get_memory_locations(self, location: int) -> Iterable[int]:
        location |= self.get_or_mask()
        mask_bit_offset = len(self.mask) - 1
        flip_bits = [ *map(lambda match: mask_bit_offset - match.start(), xRegex.finditer(self.mask)) ]
        for case in range(1 << len(flip_bits)):
            current_location = location
            for index, flipBit in enumerate(flip_bits):
                current_location &= ~(1 << flipBit)
                new_bit = ((1 << index) & case) >> index
                current_location |= new_bit << flipBit
            yield current_location


def solve(instructions: List[Instruction]) -> Tuple[int,int]:
    return (
        run_computer(ValueMaskComputer(), instructions),
        run_computer(MemoryMaskComputer(), instructions)
    )


def get_input(file_path: str) -> List[Instruction]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ Instruction(line) for line in file.readlines() ]


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