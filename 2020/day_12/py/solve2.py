#! /usr/bin/python3
from typing import NamedTuple

from common import getInput, Coordinate, InstructionType, cardinalSteps, Rotate, getPositive


class State(NamedTuple):
    coordinate: Coordinate
    waypoint: Coordinate

    def __str__(self):
        return f"Pos: {self.coordinate}  Way: {self.waypoint}"


def calculateCardinalMove(cardinal, value, waypoint):
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


def processInstruction(instruction, state):
    if instruction.type == InstructionType.Cardinal:
        return State(state.coordinate, calculateCardinalMove(instruction.cardinal, instruction.value, state.waypoint))
    if instruction.type == InstructionType.Rotate:
        return State(state.coordinate, calculateRotation(instruction.rotate, instruction.value, state.waypoint))
    if instruction.type == InstructionType.Move:
        return State(calculateMove(state.coordinate, state.waypoint, instruction.value), state.waypoint)


def main():
    state = State(Coordinate(0,0), Coordinate(-1, 10))
    print("Initial State:", state)

    for instruction in getInput():
        state = processInstruction(instruction, state)

    print("Final state:", state)
    result = getPositive(state.coordinate.latitude) + getPositive(state.coordinate.longitude)
    print("Result:", result)



if __name__ == "__main__":
    main()
