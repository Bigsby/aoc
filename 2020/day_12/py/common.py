import sys, os, re
from enum import Enum
from typing import NamedTuple


lineRegex = re.compile(r"^(?P<direction>[NSEWLRF])(?P<value>\d+)$")


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


def getPositive(value):
    return value if value >= 0 else -value


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for line in file.readlines():
            match = lineRegex.match(line)
            if (match):
                yield Instruction(match.group("direction"), match.group("value"))
