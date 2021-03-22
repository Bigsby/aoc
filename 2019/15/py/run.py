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

    def clone(self):
        cloneComputer = IntCodeComputer([])
        cloneComputer.memory = dict(self.memory)
        cloneComputer.pointer = self.pointer
        cloneComputer.base = self.base
        return cloneComputer


def drawArea(oxygen: List[Position], walls: List[Position], openSpaces: List[Position]):
    allPosiitons = walls + oxygen
    minX = int(min(map(lambda p: p.real, allPosiitons)))
    maxX = int(max(map(lambda p: p.real, allPosiitons)))
    minY = int(min(map(lambda p: p.imag, allPosiitons)))
    maxY = int(max(map(lambda p: p.imag, allPosiitons)))
    for y in range(maxY, minY - 1, - 1):
        for x in range(minX, maxX + 1):
            position = x + y * 1j
            c = " "
            if position in walls:
                c = "#"
            if position in openSpaces:
                c = "."
            if position in oxygen:
                c = "O"
            print(c, end="")
        print()
    print()


def runUntilOxygenSystem(memory: List[int]) -> Tuple[int, Position, List[Position]]:
    startPosition = 0j
    openSpaces: List[Position] = []
    oxygenPosition = 0j
    queue = [(startPosition, [startPosition], IntCodeComputer(memory))]
    visited = [startPosition]
    stepsToOxygenSystem = 0
    while queue:
        position, path, droid = queue.pop(0)
        for command, direction in DIRECTIONS.items():
            newPosition = position + direction
            if newPosition not in visited:
                visited.append(newPosition)
                newDroid = droid.clone()
                newDroid.inputs.append(command)
                while not newDroid.outputing:
                    newDroid.tick()
                status = newDroid.getOutput()
                if status == 2:  # Oxygen system
                    if stepsToOxygenSystem == 0:
                        stepsToOxygenSystem = len(path)
                    oxygenPosition = newPosition
                elif status == 1:  # Open space
                    openSpaces.append(newPosition)
                    while not newDroid.polling:
                        newDroid.tick()
                    newPath = list(path)
                    newPath.append(newPosition)
                    queue.append((newPosition, newPath, newDroid))
    return stepsToOxygenSystem, oxygenPosition, openSpaces


def solve(memory: List[int]) -> Tuple[int, int]:
    stepsToOxygenSystem, oxygenSystemPosition, openSpaces = runUntilOxygenSystem(
        memory)
    filled = [oxygenSystemPosition]
    minutes = 0
    while openSpaces:
        minutes += 1
        for oxygen in list(filled):
            for direction in DIRECTIONS.values():
                position = oxygen + direction
                if position in openSpaces:
                    filled.append(position)
                    openSpaces.remove(position)
    return stepsToOxygenSystem, minutes


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
