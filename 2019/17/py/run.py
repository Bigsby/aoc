#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
from collections import defaultdict
from itertools import permutations


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
    
    def clone(self):
        cloneComputer = IntCodeComputer([])
        cloneComputer.memory = dict(self.memory)
        cloneComputer.pointer = self.pointer
        cloneComputer.base = self.base
        return cloneComputer


DIRECTIONS = { "v": 1j, ">": 1, "^": -1j, "<": -1 }
Scafolds = List[complex]
Robot = Tuple[complex,complex]
PathStretch = Tuple[int,int]
Path = List[str]


def printArea(scafolds: Scafolds, robot: Robot):
    minX = int(min(map(lambda p: p.real, scafolds)))
    maxX = int(max(map(lambda p: p.real, scafolds)))
    minY = int(min(map(lambda p: p.imag, scafolds)))
    maxY = int(max(map(lambda p: p.imag, scafolds)))
    print(minX, maxX, minY, maxY)
    for y in range(minY, maxY + 1):
        for x in range(minX, maxX + 1):
            position = x + y * 1j
            c = "."
            if position in scafolds:
                c = "#"
            if position == robot[0]:
                c = [ c for c,direction in DIRECTIONS.items() if direction == robot[1]][0]
            print(c, end="")
        print()
    print()


def getScafoldsAndRobot(asciiComputer: IntCodeComputer) -> Tuple[Scafolds,Robot]:
    position = 0j
    scafolds: List[complex] = []
    robot = (0j, 0j)
    while asciiComputer.running:
        asciiComputer.tick()
        if asciiComputer.outputing:
            code = asciiComputer.getOutput()
            if code == 35: # "#"
                scafolds.append(position)
                position += 1
            elif code == 46: # "."
                position += 1
            elif code == 10: # line feed
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


TURNS = [ (-1j, "L"), (1j, "R") ]
def findPath(scafolds: Scafolds, robot: Robot) -> Path:
    path: Path = []
    currentTurn = ""
    turnFound = True
    while turnFound:
        position, direction = robot
        if position + direction not in scafolds:
            turnFound = False
            for turn, code in TURNS:
                if position + direction * turn in scafolds:
                    turnFound = True
                    currentTurn = code
                    robot = position, direction * turn
        else:
            currentLength = 0
            while position + direction in scafolds:
                position += direction    
                currentLength += 1
            robot = position, direction
            path.append(currentTurn)
            path.append(str(currentLength))
    return path


def getRepeatsInPath(path: Path, segment: Path) -> List[Tuple[int,int]]:
    return [(start, start + len(segment)) for start in range(len(path) - len(segment) + 1) if path[start:start + len(segment)] == segment]


def isPermutationValid(path: Path, permutation: Tuple[Tuple[int,int],...]) -> bool:
    path = list(path)
    for length, repeatCount in permutation:
        segment = path[:length]
        if len(segment) * 2 - 1 > 20:
            return False
        repeatIndexes = getRepeatsInPath(path, segment)
        if len(repeatIndexes) != repeatCount:
            return False
        repeatIndexes.reverse()
        for start, _ in repeatIndexes:
            for _ in range(length):
                del path[start]
    return not path


def getRoutines(path: Path) -> Dict[int,Tuple[Path,List[Tuple[int,int]]]]:
    routines = {}
    for permutation in permutations([(6,4), (10, 3), (8, 3), (6,3)], 3): # possible (length, repeat counts)
        if isPermutationValid(path, permutation):
            indexesToGroup = [ i for i in range(len(path))]
            for c, (length, _) in enumerate(permutation):
                index = min(indexesToGroup)
                segment = path[index:index + length]
                repeatIndexes = getRepeatsInPath(path, segment)
                routines[c + ord("A")] = segment, repeatIndexes
                for start, end in repeatIndexes:
                    for i in range(start, end):
                        indexesToGroup.remove(i)
            break
    return routines


def part2(memory: List[int], scafolds: Scafolds, robot: Robot) -> int:
    asciiComputer = IntCodeComputer(memory)
    asciiComputer.memory[0] = 2
    path = findPath(scafolds, robot)
    routines = getRoutines(path)
    mainRoutineSegments = {}
    inputs = []
    for routine, (segements, indexes) in routines.items():
        inputs.append(",".join(segements) + chr(10))
        for indexGroup in indexes:
            mainRoutineSegments[indexGroup[0]] = routine
    inputs.insert(0, ",".join([ chr(routine) for _, routine in sorted(mainRoutineSegments.items()) ]) + chr(10))
    inputs.append("n" + chr(10))
    for inputLine in inputs:
        for c in inputLine:
            asciiComputer.inputs.append(ord(c))
    return asciiComputer.runUntilHalt().pop()


def solve(memory: List[int]) -> Tuple[int,int]:
    asciiComputer = IntCodeComputer(memory)
    scafolds, robot = getScafoldsAndRobot(asciiComputer)
    return (
        part1(scafolds),
        part2(memory, scafolds, robot)
    )


def getInput(filePath: str) -> List[int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ int(i) for i in file.read().split(",") ]


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