#! /usr/bin/python3

import sys, os, time
from typing import Dict
from collections import defaultdict

InfectionStatus = Dict[complex,bool]


def part1(state: InfectionStatus) -> int:
    state = defaultdict(bool, state.items())
    infectionCount = 0
    currentNode = max(n.real for n in state.keys()) // 2 + (min(n.imag for n in state.keys()) // 2)* 1j
    direction = 1j
    for _ in range(10000):
        nodeState = state[currentNode]
        direction *= -1j if nodeState else 1j
        state[currentNode] = not nodeState
        currentNode += direction
        infectionCount += not nodeState
    return infectionCount


CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3
STATE_DIRECTIONS = [
    1j,
    1,
    -1j,
    -1
]
STATE_TRANSITIONS = [
    WEAKENED,
    INFECTED,
    FLAGGED,
    CLEAN
]
def part2(state: InfectionStatus) -> int:
    quadState: Dict[complex,int] = defaultdict(lambda: CLEAN,[ (node, INFECTED if value else CLEAN) for node, value in state.items() ])
    currentNode = max(n.real for n in state.keys()) // 2 + (min(n.imag for n in state.keys()) // 2)* 1j
    direction = 1j
    infectionCount = 0
    for _ in range(10000000):
        nodeState = quadState[currentNode]
        newState = STATE_TRANSITIONS[nodeState]
        direction *= STATE_DIRECTIONS[nodeState]
        quadState[currentNode] = newState
        currentNode += direction
        infectionCount += newState == INFECTED
    return infectionCount


def getInput(filePath: str) -> InfectionStatus:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        infectionStatus: InfectionStatus = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                infectionStatus[x - y *1j] = c == "#"
        return infectionStatus


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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()