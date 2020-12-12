#! /usr/bin/python3

from typing import NamedTuple

from common import getInput, Coordinate, Cardinal, Rotate, InstructionType, getPositive, cardinalSteps


class State(NamedTuple):
    heading: Cardinal
    coordinate: Coordinate

    def __str__(self):
        return f"{self.coordinate} {self.heading}"


cardinalDegrees = {
    Cardinal.North: 0,
    Cardinal.South: 180,
    Cardinal.East: 90,
    Cardinal.West: 270
}


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
    result = degreesToCardinal(newValue)
    return degreesToCardinal(newValue)


def calculateMove(start, heading, value):
    step = cardinalSteps[heading]
    return Coordinate(start.latitude + step.latitude * value, start.longitude + step.longitude * value)
    
def processInstruction(instruction, state):
    if instruction.type == InstructionType.Cardinal:
        return State(state.heading, calculateMove(state.coordinate, instruction.cardinal, instruction.value))
    if instruction.type == InstructionType.Rotate:
        return State(calculateHeading(state.heading, instruction.rotate, instruction.value), state.coordinate)
    if instruction.type == InstructionType.Move:
        return State(state.heading, calculateMove(state.coordinate, state.heading, instruction.value))


def main():
    state = State(Cardinal.East, Coordinate(0,0))
    print("Initial State:", state)

    for instruction in getInput():
        state = processInstruction(instruction, state)

    print("Final state:", state)
    result = getPositive(state.coordinate.latitude) + getPositive(state.coordinate.longitude)
    print("Result:", result)


if __name__ == "__main__":
    main()
