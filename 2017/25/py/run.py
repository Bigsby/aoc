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


setup_regex = re.compile(
    r"^Begin in state (?P<state>\w).*\s+^[^\d]*(?P<steps>\d+)", re.MULTILINE)
state_regex = re.compile(
    r"^In state (?P<state>\w):\n.*If.*\n[^\d]*(?P<fValue>\d).\n.*(?P<fSlot>right|left).\n.*state (?P<fState>\w).\n.*If.*\n[^\d]*(?P<tValue>\d).\n.*(?P<tSlot>right|left).\n.*state (?P<tState>\w)", re.MULTILINE)


def get_input(file_path: str) -> Tuple[str, int, States]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    states: States = {}
    initial_state = ""
    steps = 0
    with open(file_path, "r") as file:
        for split in file.read().split("\n\n"):
            setup_match = setup_regex.match(split)
            if setup_match:
                initial_state = setup_match.group("state")
                steps = int(setup_match.group("steps"))
                continue
            state_match = state_regex.match(split)
            if state_match:
                states[state_match.group("state")] = \
                    ((
                        int(state_match.group("fValue")),
                        1 if state_match.group("fSlot") == "right" else -1,
                        state_match.group("fState")
                    ),
                    (
                        int(state_match.group("tValue")),
                        1 if state_match.group("tSlot") == "right" else -1,
                        state_match.group("tState")
                    ))
    return initial_state, steps, states


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
