#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
from collections import defaultdict
import re
from itertools import combinations


class IntCodeComputer():
    def __init__(self, memory: List[int], inputs: List[int] = [], defaultInput:bool = False, defaultValue: int = -1):
        self.memory = defaultdict(int, [ (index, value) for index, value in enumerate(memory) ])
        self.pointer = 0
        self.inputs = inputs
        self.outputs = [ ]
        self.base = 0
        self.running = True
        self.polling = False
        self.paused = False
        self.outputing = False
        self.defaultInput = defaultInput
        self.defaultValue = defaultValue
    
    def setInput(self, value: int):
        self.inputs.insert(0, value)
    
    def runUntilHalt(self) -> List[int]:
        while self.running:
            self.tick()
        return self.outputs
    
    def runUntilPaused(self):
        self.paused = False
        while not self.paused and self.running:
            self.tick()
        return self
    
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
            elif self.defaultInput:
                self.memory[self.getAddress(1, p1mode)] = self.defaultValue
                self.pointer += 2
                self.polling = True
            else:
                self.paused = True
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
        cloneComputer.running = self.running
        cloneComputer.polling = self.polling
        cloneComputer.paused = self.paused
        cloneComputer.outputing = self.outputing
        return cloneComputer


def parseRoomOutput(output:str) -> Tuple[str,List[str],List[str]]:
    stage = 0
    room = ""
    doors = []
    items = []
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


def runCommand(droid: IntCodeComputer, command: str):
    if command != "":
        for c in command + '\n':
            droid.inputs.append(ord(c))
    droid.runUntilPaused()
    output = "".join(chr(c) for c in droid.outputs)
    droid.outputs.clear()
    return output


# use to play manually
def manualScout(memory: List[int]):
    print("Scounting")
    droid = IntCodeComputer(memory)
    command = ""
    while command != "quit" and droid.running:
        output = runCommand(droid, command)
        print(parseRoomOutput(output))
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
def navigateRooms(droid: IntCodeComputer, command: str, destination: str, pickupItems: bool):
    visited = []
    wayIn = {}
    lastDirection = ""
    pressureRoomWayIn = ""
    inventory = []
    while droid.running:
        output = runCommand(droid, command)
        room, doors, items = parseRoomOutput(output)
        if room == destination:
            break
        if room == PRESSURE_ROOM:
            pressureRoomWayIn = lastDirection
        if room not in wayIn:
            wayIn[room] = lastDirection
        if pickupItems:
            for item in items:
                if item not in FORBIDEN_ITEMS:
                    output = runCommand(droid, TAKE + item)
                    inventory.append(item)
        newDoor = False
        for door in doors:
            if (room, door) not in visited:
                if door == WAY_INVERSE[wayIn[room]]:
                    continue
                newDoor = True
                visited.append((room, door))
                command = lastDirection = door
                break
        if not newDoor:
            if wayIn[room] == "":
                # assume that first room only has 1 door
                command = doors[0]
                break
            command = WAY_INVERSE[wayIn[room]]
    return command, inventory, pressureRoomWayIn


DROP = "drop "
def findPassword(memory: List[int]):
    droid = IntCodeComputer(memory)
    # navigate all rooms and pickup non-forbiden items
    command, inventory, pressureRoomWayIn = navigateRooms(droid, "", "", True)
    # go to Security Checkpoint
    _ = navigateRooms(droid, command, SECURITY_CHECKPOINT, False)    
    # test combinations of items
    for item in inventory:
        runCommand(droid, DROP + item)
    previousInventory = tuple()
    for newInventory in combinations(inventory, 4):
        for item in newInventory:
            if item not in previousInventory:
                runCommand(droid, TAKE + item)
        for item in previousInventory:
            if item not in newInventory:
                runCommand(droid, DROP + item)
        output = runCommand(droid, pressureRoomWayIn)
        passwordMatch = re.search(r"typing (?P<password>\d+)", output)
        if passwordMatch:
            return passwordMatch.group("password")
        previousInventory = newInventory


def part1(memory: List[int]):
    return findPassword(memory)


def part2(puzzleInput):
    pass


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