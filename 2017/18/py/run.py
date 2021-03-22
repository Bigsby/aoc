#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
from collections import defaultdict

Instruction = Tuple[str, List[str]]


class Program:
    def __init__(self, instructions: List[Instruction], id: int, outputOnRcv: bool = False) -> None:
        self.instructions = instructions
        self.id = id
        self.outputOnRcv = outputOnRcv
        self.registers: Dict[str, int] = defaultdict(int)
        self.registers["p"] = id
        self.pointer = 0
        self.outputs: List[int] = []
        self.inputs: List[int] = []
        self.running = True
        self.outputting = False
        self.polling = False
        self.outputCount = 0
        self.params: List[str] = []

    def _getValue(self, offset: int) -> int:
        value = self.params[offset]
        try:
            return int(value)
        except:
            return self.registers[value]

    def tick(self):
        if self.running:
            mnemonic, self.params = self.instructions[self.pointer]
            self.pointer += 1
            if mnemonic == "set":
                self.registers[self.params[0]] = self._getValue(1)
            elif mnemonic == "add":
                self.registers[self.params[0]] += self._getValue(1)
            elif mnemonic == "mul":
                self.registers[self.params[0]] *= self._getValue(1)
            elif mnemonic == "mod":
                self.registers[self.params[0]] %= self._getValue(1)
            elif mnemonic == "snd":
                self.outputCount += 1
                self.outputs.append(self._getValue(0))
            elif mnemonic == "rcv":
                if self.outputOnRcv:
                    self.outputting = True
                elif self.inputs:
                    self.polling = False
                    self.registers[self.params[0]] = self.inputs.pop(0)
                else:
                    self.polling = True
                    self.pointer -= 1
            elif mnemonic == "jgz" and self._getValue(0) > 0:
                self.pointer += self._getValue(1) - 1
        self.running = self.pointer < len(self.instructions)

    def isActive(self):
        return self.running and not self.polling


def part1(instructions: List[Instruction]) -> int:
    program = Program(instructions, 0, True)
    while not program.outputting:
        program.tick()
    return program.outputs[-1]


def part2(instructions: List[Instruction]) -> int:
    program0 = Program(instructions, 0)
    program1 = Program(instructions, 1)
    program1.inputs = program0.outputs
    program0.inputs = program1.outputs
    while program0.isActive() or program1.isActive():
        program0.tick()
        program1.tick()
    return program1.outputCount


def solve(instructions: List[Instruction]) -> Tuple[int, int]:
    return (
        part1(instructions),
        part2(instructions)
    )


def parseLine(line: str) -> Instruction:
    mnemonic, *params = line.split(" ")
    return mnemonic, params


def getInput(filePath: str) -> List[Instruction]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        return [parseLine(line.strip()) for line in file.readlines()]


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
