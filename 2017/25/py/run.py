#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, Tuple
import re
from collections import defaultdict

Next = Tuple[int, int, str]
States = Dict[str, Tuple[Next, Next]]


def solve(data: Tuple[str, int, States]) -> Tuple[int, str]:
    state, steps, states = data
    cursor = 0
    tape: Dict[int, int] = defaultdict(int)
    for _ in range(steps):
        value, direction, state = states[state][tape[cursor]]
        tape[cursor] = value
        cursor += direction
    return sum(tape.values()), ""


setupRegex = re.compile(
    r"^Begin in state (?P<state>\w).*\s+^[^\d]*(?P<steps>\d+)", re.MULTILINE)
stateRegex = re.compile(
    r"^In state (?P<state>\w):\n.*If.*\n[^\d]*(?P<fValue>\d).\n.*(?P<fSlot>right|left).\n.*state (?P<fState>\w).\n.*If.*\n[^\d]*(?P<tValue>\d).\n.*(?P<tSlot>right|left).\n.*state (?P<tState>\w)", re.MULTILINE)


def getInput(filePath: str) -> Tuple[str, int, States]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    states = States()
    initialState = ""
    steps = 0
    with open(filePath, "r") as file:
        for split in file.read().split("\n\n"):
            setupMatch = setupRegex.match(split)
            if setupMatch:
                initialState = setupMatch.group("state")
                steps = int(setupMatch.group("steps"))
                continue
            stateMatch = stateRegex.match(split)
            if stateMatch:
                states[stateMatch.group("state")] = \
                    ((int(stateMatch.group("fValue")), 1 if stateMatch.group("fSlot") == "right" else -1, stateMatch.group("fState")),
                     (int(stateMatch.group("tValue")), 1 if stateMatch.group("tSlot") == "right" else -1, stateMatch.group("tState")))
    return initialState, steps, states


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
