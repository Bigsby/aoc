#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from collections import defaultdict
from enum import Enum


class IntCodeComputer():
    def __init__(self, memory: List[int], inputs: List[int] = []):
        self.memory = defaultdict(int, [ (index, value) for index, value in enumerate(memory) ])
        self.pointer = 0
        self.inputs = inputs
        self.outputs = [ ]
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
        if mode == 0: # POSITION
            return self.memory[value]
        if mode == 1: # IMMEDIATE
            return value
        elif mode == 2: # RELATIVE
            return self.memory[self.base + value]
        raise Exception("Unrecognized parameter mode", mode)
    
    def getAddress(self, offset: int, mode: int) -> int:
        value = self.memory[self.pointer + offset]
        if mode == 0: # POSITION
            return value
        if mode == 2: # RELATIVE
            return self.base + value
        raise Exception("Unrecognized address mode", mode)


    def getOutput(self) -> int:
        self.outputing = False
        return self.outputs.pop()
    
    def addInput(self, value: int):
        self.inputs.append(value)

    def tick(self):
        instruction = self.memory[self.pointer]
        opcode, p1mode, p2mode, p3mode = instruction % 100, (instruction // 100) % 10, (instruction // 1000) % 10, (instruction // 10000) % 10
        if not self.running:
            return
        if opcode == 1: # ADD
            self.memory[self.getAddress(3, p3mode)] = self.getParameter(1, p1mode) + self.getParameter(2, p2mode)
            self.pointer += 4
        elif opcode == 2: # MUL
            self.memory[self.getAddress(3, p3mode)] = self.getParameter(1, p1mode) * self.getParameter(2, p2mode)
            self.pointer += 4
        elif opcode == 3: # INPUT
            if self.inputs:
                self.polling = False
                self.memory[self.getAddress(1, p1mode)] = self.inputs.pop(0)
                self.pointer += 2
            else:
                self.polling = True
        elif opcode == 4: # OUTPUT
            self.outputing = True
            self.outputs.append(self.getParameter(1, p1mode))
            self.pointer += 2
        elif opcode == 5: # JMP_TRUE
            if self.getParameter(1, p1mode):
                self.pointer = self.getParameter(2, p2mode)
            else:
                self.pointer += 3
        elif opcode == 6: # JMP_FALSE
            if not self.getParameter(1, p1mode):
                self.pointer = self.getParameter(2, p2mode)
            else:
                self.pointer += 3
        elif opcode == 7: # LESS_THAN
            self.memory[self.getAddress(3, p3mode)] = 1 if self.getParameter(1, p1mode) < self.getParameter(2, p2mode) else 0
            self.pointer += 4
        elif opcode == 8: # EQUALS
            self.memory[self.getAddress(3, p3mode)] = 1 if self.getParameter(1, p1mode) == self.getParameter(2, p2mode) else 0
            self.pointer += 4
        elif opcode == 9: # SET_BASE
            self.base += self.getParameter(1, p1mode)
            self.pointer += 2
        elif opcode == 99: # HALT
            self.running = False
        else:
            raise Exception(f"Unknown instruction", self.pointer, instruction, opcode, p1mode, p2mode, p3mode)
    
    def __str__(self):
        return f"s {self.running} p {self.pointer} i {self.inputs} o {self.outputs}"


class Tile(Enum):
    Empty = 0
    Wall = 1
    Block = 2
    Paddle = 3
    Ball = 4

TILE_CHARS = {
    Tile.Empty: ".",
    Tile.Wall: "W",
    Tile.Block: "B",
    Tile.Paddle: "P",
    Tile.Ball: "X"
}
def printScreen(screen: Dict[complex,Tile]):
    maxX = int(max(map(lambda p: p.real, screen.keys())))
    minX = int(min(map(lambda p: p.real, screen.keys())))
    maxY = int(max(map(lambda p: p.imag, screen.keys())))
    minY = int(min(map(lambda p: p.imag, screen.keys())))
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            c = " "
            position = x + y * 1j
            if position in screen:
                c = TILE_CHARS[screen[position]]
            print(c, end="")
        print()
    print()


def runGame(memory: List[int]) -> Tuple[int,int]:
    cabinet = IntCodeComputer(memory)
    screen: Dict[complex,Tile] = {}
    currentOuput = []
    ball = 0
    paddle = 0
    score = 0
    while cabinet.running:
        cabinet.tick()
        if cabinet.polling:
            joystick = 0
            if ball > paddle:
                joystick = 1
            elif ball < paddle:
                joystick = -1
            cabinet.inputs.append(joystick)
        if cabinet.outputing:
            currentOuput.append(cabinet.getOutput())
            if len(currentOuput) == 3:
                value = currentOuput.pop()
                y = currentOuput.pop()
                x = currentOuput.pop()
                position = x + y * 1j
                if position == -1:
                    score = value
                else: 
                    tile = Tile(value)
                    if tile == Tile.Ball:
                        ball = x
                    elif tile == Tile.Paddle:
                        paddle = x
                    screen[x + y * 1j] = tile
    return list(screen.values()).count(Tile.Block), score    

def part1(memory: List[int]):
    blocks, _ = runGame(memory)
    return blocks
    # cabinet = IntCodeComputer(memory)
    # screen: Dict[complex,Tile] = {}
    # currentOuput = []
    # while cabinet.running:
    #     cabinet.tick()
    #     if cabinet.outputing:
    #         currentOuput.append(cabinet.getOutput())
    #         if len(currentOuput) == 3:
    #             tile = Tile(currentOuput.pop())
    #             y = currentOuput.pop()
    #             x = currentOuput.pop()
    #             screen[x + y * 1j] = tile
    


def part2(memory: List[int]):
    memory[0] = 2
    _, score = runGame(memory)
    return score
    # cabinet = IntCodeComputer(memory)
    # screen: Dict[complex,Tile] = {}
    # currentOuput = []
    # ball = 0
    # paddle = 0
    # score = 0
    # while cabinet.running:
    #     cabinet.tick()
    #     if cabinet.polling:
    #         joystick = 0
    #         if ball > paddle:
    #             joystick = 1
    #         elif ball < paddle:
    #             joystick = -1
    #         cabinet.inputs.append(joystick)
    #     if cabinet.outputing:
    #         currentOuput.append(cabinet.getOutput())
    #         if len(currentOuput) == 3:
    #             value = currentOuput.pop()
    #             y = currentOuput.pop()
    #             x = currentOuput.pop()
    #             position = x + y * 1j
    #             if position == -1:
    #                 score = value
    #             else: 
    #                 tile = Tile(value)
    #                 if tile == Tile.Ball:
    #                     ball = x
    #                 elif tile == Tile.Paddle:
    #                     paddle = x
    #                 screen[x + y * 1j] = tile
    
    # return score


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().split(",") ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()