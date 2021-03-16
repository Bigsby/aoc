#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re

State = List[int]
Notes = Dict[int, int]


def get_state_value(index: int, state: State) -> int:
    return sum([1 << i for i in range(5) if i + index - 2 in state])


def run_generations(state: State, notes: Notes, generations: int) -> State:
    generation = 0
    while generation < generations:
        state = [index for index in range(
            min(state) - 2, max(state) + 2) if notes[get_state_value(index, state)]]
        generation += 1
    return state


def part2(state: State, notes: Notes) -> int:
    jump = 200
    first_state = run_generations(state, notes, jump)
    first_sum = sum(first_state)
    second_state = run_generations(first_state, notes, jump)
    diff = sum(second_state) - first_sum
    target = 5 * 10 ** 10
    return first_sum + diff * (target // jump - 1)


def solve(puzzle_input: Tuple[State, Notes]) -> Tuple[int, int]:
    state, notes = puzzle_input
    return (
        sum(run_generations(state, notes, 20)),
        part2(state, notes)
    )


def parse_initial_state(line: str) -> List[int]:
    return [index for index, c in enumerate(line[15:]) if c == "#"]


def compute_pattern(pattern: str) -> int:
    return sum([1 << index for index, c in enumerate(pattern) if c == "#"])


notes_regex = re.compile(
    r"^(?P<pattern>[#\.]{5})\s=>\s(?P<result>[#\.])$", re.MULTILINE)


def parse_notes(note_lines: str) -> Notes:
    return {compute_pattern(match.group("pattern")): 1 if match.group("result") == "#" else 0
            for match in notes_regex.finditer(note_lines)}


def get_input(file_path: str) -> Tuple[State, Notes]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        initial_state_line, note_lines = file.read().split("\n\n")
        return parse_initial_state(initial_state_line), parse_notes(note_lines)


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
