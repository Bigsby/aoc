#! /usr/bin/python3

import sys, os, time
import re
from enum import Enum
from typing import NamedTuple


class Cardinal(Enum):
    North = "N"
    South = "S"
    East = "E"
    West = "W"


class Rotate(Enum):
    Left = "L"
    Right = "R"
 

class Move(Enum):
    Forward = "F"


class InstructionType(Enum):
    Cardinal = 0
    Rotate = 1
    Move = 2


def getEnumValueList(cls):
    return [ e.value for e in cls ]


class Coordinate(NamedTuple):
    latitude: int
    longitude: int
    
    def __str__(self):
        return f"{self.latitude} {self.longitude}"


cardinals = getEnumValueList(Cardinal)
rotates = getEnumValueList(Rotate)
moves = getEnumValueList(Move)


cardinalSteps = {
    Cardinal.North: Coordinate(-1, 0),
    Cardinal.South: Coordinate(1, 0),
    Cardinal.East: Coordinate(0, 1),
    Cardinal.West: Coordinate(0, -1)
}


class Instruction():
    def __init__(self, direction, value):
        self.value = int(value)
        if direction in cardinals:
            self.type = InstructionType.Cardinal
            self.cardinal = Cardinal(direction)
        elif direction in rotates:
            self.type = InstructionType.Rotate
            self.rotate = Rotate(direction)
        elif direction in moves:
            self.type = InstructionType.Move
            self.move = Move(direction)
        else:
            raise Exception(f"Unknow direction: {direction}")

    def __str__(self):
        if self.type == InstructionType.Cardinal:
            return f"{self.cardinal} {self.value}"
        if self.type == InstructionType.Rotate:
            return f"{self.rotate} {self.value}"
        if self.type == InstructionType.Move:
            return f"{self.move} {self.value}"


def degreesToCardinal(degrees):
    if degrees == 0:
        return Cardinal.North
    if degrees == 90:
        return Cardinal.East
    if degrees == 180:
        return Cardinal.South
    if degrees == 270:
        return Cardinal.West
    raise Exception(f"Unknown degrees {degrees}")


cardinalDegrees = {
    Cardinal.North: 0,
    Cardinal.South: 180,
    Cardinal.East: 90,
    Cardinal.West: 270
}
rotateDirection = {
    Rotate.Left: -1,
    Rotate.Right: 1
}
def calculateHeading(start, rotate, value):
    direction = rotateDirection[rotate]
    currentValue = cardinalDegrees[start]
    newValue = currentValue + value * direction
    if newValue < 0:
        newValue = 360 + newValue
    elif newValue > 270:
        newValue = newValue - 360
    return degreesToCardinal(newValue)


def calculateMove1(start, heading, value):
    step = cardinalSteps[heading]
    return Coordinate(start.latitude + step.latitude * value, start.longitude + step.longitude * value)
    
def processInstruction1(instruction, state):
    heading, coordinate = state
    if instruction.type == InstructionType.Cardinal:
        return (heading, calculateMove1(coordinate, instruction.cardinal, instruction.value))
    if instruction.type == InstructionType.Rotate:
        return (calculateHeading(heading, instruction.rotate, instruction.value), coordinate)
    if instruction.type == InstructionType.Move:
        return (heading, calculateMove1(coordinate, heading, instruction.value))


def part1(puzzleInput):
    state = (Cardinal.East, Coordinate(0,0))
    for instruction in puzzleInput:
        state = processInstruction1(instruction, state)
    return abs(state[1].latitude) + abs(state[1].longitude)


def calculateCardinalMove2(cardinal, value, waypoint):
    step = cardinalSteps[cardinal]
    return Coordinate(waypoint.latitude + step.latitude * value, waypoint.longitude + step.longitude * value)

rotationSteps = {
    Rotate.Left: Coordinate(-1, 1),
    Rotate.Right: Coordinate(1, -1)
}

def calculateRotation(direction, value, waypoint):
    step = rotationSteps[direction]
    while value:
        waypoint = Coordinate(step.latitude * waypoint.longitude, step.longitude * waypoint.latitude)
        value -= 90
    return waypoint


def calculateMove(coordinate, waypoint, value):
    return Coordinate(coordinate.latitude + waypoint.latitude * value, coordinate.longitude + waypoint.longitude * value)


def processInstruction2(instruction, state):
    coordinate, waypoint = state
    if instruction.type == InstructionType.Cardinal:
        return (coordinate, calculateCardinalMove2(instruction.cardinal, instruction.value, waypoint))
    if instruction.type == InstructionType.Rotate:
        return (coordinate, calculateRotation(instruction.rotate, instruction.value, waypoint))
    if instruction.type == InstructionType.Move:
        return (calculateMove(coordinate, waypoint, instruction.value), waypoint)


def part2(puzzleInput):
    state = (Coordinate(0,0), Coordinate(-1, 10))
    for instruction in puzzleInput:
        state = processInstruction2(instruction, state)
    return abs(state[0].latitude) + abs(state[0].longitude)


lineRegex = re.compile(r"^(?P<direction>[NSEWLRF])(?P<value>\d+)$")
def parseLine(line):
    match = lineRegex.match(line)
    return Instruction(match.group("direction"), match.group("value"))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]
            

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