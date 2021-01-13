#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re

State = List[int]
Notes = Dict[int,int]


def getStateValue(index: int, state: State):
    return sum([ 2 ** i for i in range(5) if i + index - 2 in state ])


def runGenerations(puzzleInput: Tuple[State,Notes], generations: int) -> List[int]:
    state, notes = puzzleInput
    generation = 0
    while generation < generations:
        state = [ index for index in range(min(state) - 2, max(state) + 2) if notes[getStateValue(index, state)] ]
        generation += 1
    return state


def part1(puzzleInput: Tuple[State,Notes]) -> int:
    return sum(runGenerations(puzzleInput, 20))


def part2(puzzleInput: Tuple[State,Notes]) -> int:
    jump = 200
    firstState = runGenerations(puzzleInput, jump)
    firstSum = sum(firstState)
    secondState = runGenerations((firstState, puzzleInput[1]), jump)
    diff = sum(secondState) - firstSum
    target = 5 * 10 ** 10
    return firstSum + diff * ( target // jump - 1)


initialStateRegex = re.compile(r"#|\.")
def parseInitialState(line: str) -> List[int]:
    return [ index for index, match in enumerate(initialStateRegex.finditer(line)) if match.group() == "#" ]


def computePattern(pattern: str) -> int:
    return sum([ 2**index for index, c in enumerate(pattern) if c == "#" ] )

notesRegex = re.compile(r"^(?P<pattern>[#\.]{5})\s=>\s(?P<result>[#\.])$", re.MULTILINE)
def parseNotes(noteLines: str) -> Notes:
    return { computePattern(match.group("pattern")): 1 if match.group("result") == "#" else 0 for match in notesRegex.finditer(noteLines) }


def getInput(filePath: str) -> Tuple[State,Notes]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        initialStateLine, noteLines = file.read().split("\n\n")
        return parseInitialState(initialStateLine), parseNotes(noteLines)


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
