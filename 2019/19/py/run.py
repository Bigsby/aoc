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

    def setInput(self, value: int):
        self.inputs.insert(0, value)

    def runUntilHalt(self) -> List[int]:
        while self.running:
            self.tick()
        return self.outputs

    def getParameter(self, offset: int, mode: int) -> int:
        value = self.memory[self.pointer + offset]
        if mode == 0:  # POSITION
            return self.memory[value]
        if mode == 1:  # IMMEDIATE
            return value
        elif mode == 2:  # RELATIVE
            return self.memory[self.base + value]
        raise Exception("Unrecognized parameter mode", mode)

    def getAddress(self, offset: int, mode: int) -> int:
        value = self.memory[self.pointer + offset]
        if mode == 0:  # POSITION
            return value
        if mode == 2:  # RELATIVE
            return self.base + value
        raise Exception("Unrecognized address mode", mode)

    def getOutput(self) -> int:
        self.outputing = False
        return self.outputs.pop()

    def addInput(self, value: int):
        self.inputs.append(value)

    def tick(self):
        instruction = self.memory[self.pointer]
        opcode, p1mode, p2mode, p3mode = instruction % 100, (
            instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10
        if not self.running:
            return
        if opcode == 1:  # ADD
            self.memory[self.getAddress(3, p3mode)] = self.getParameter(
                1, p1mode) + self.getParameter(2, p2mode)
            self.pointer += 4
        elif opcode == 2:  # MUL
            self.memory[self.getAddress(3, p3mode)] = self.getParameter(
                1, p1mode) * self.getParameter(2, p2mode)
            self.pointer += 4
        elif opcode == 3:  # INPUT
            if self.inputs:
                self.polling = False
                self.memory[self.getAddress(1, p1mode)] = self.inputs.pop(0)
                self.pointer += 2
            else:
                self.polling = True
        elif opcode == 4:  # OUTPUT
            self.outputing = True
            self.outputs.append(self.getParameter(1, p1mode))
            self.pointer += 2
        elif opcode == 5:  # JMP_TRUE
            if self.getParameter(1, p1mode):
                self.pointer = self.getParameter(2, p2mode)
            else:
                self.pointer += 3
        elif opcode == 6:  # JMP_FALSE
            if not self.getParameter(1, p1mode):
                self.pointer = self.getParameter(2, p2mode)
            else:
                self.pointer += 3
        elif opcode == 7:  # LESS_THAN
            self.memory[self.getAddress(3, p3mode)] = 1 if self.getParameter(
                1, p1mode) < self.getParameter(2, p2mode) else 0
            self.pointer += 4
        elif opcode == 8:  # EQUALS
            self.memory[self.getAddress(3, p3mode)] = 1 if self.getParameter(
                1, p1mode) == self.getParameter(2, p2mode) else 0
            self.pointer += 4
        elif opcode == 9:  # SET_BASE
            self.base += self.getParameter(1, p1mode)
            self.pointer += 2
        elif opcode == 99:  # HALT
            self.running = False
        else:
            raise Exception(f"Unknown instruction", self.pointer,
                            instruction, opcode, p1mode, p2mode, p3mode)


def isPositionInBeam(memory: List[int], x: int, y: int) -> int:
    robot = IntCodeComputer(memory)
    robot.inputs.append(x)
    robot.inputs.append(y)
    while not robot.outputing:
        robot.tick()
    return robot.getOutput()


def part1(memory: List[int]) -> int:
    pointsCount = 0
    for y in range(50):
        for x in range(50):
            pointsCount += isPositionInBeam(memory, x, y)
    return pointsCount


def part2(memory: List[int]) -> int:
    y = offset = 99
    x = 0
    while True:
        while not isPositionInBeam(memory, x, y):
            x += 1
        topY = y - offset
        if isPositionInBeam(memory, x, topY) and isPositionInBeam(memory, x + offset, topY):
            return x * 10000 + topY
        y += 1


def solve(memory: List[int]) -> Tuple[int, int]:
    return (
        part1(memory),
        part2(memory)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        return [int(i) for i in file.read().split(",")]


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
