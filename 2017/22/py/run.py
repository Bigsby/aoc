#! /usr/bin/python3

import sys, os, time
from typing import Dict, Tuple
from collections import defaultdict

InfectionStatus = Dict[complex,bool]


def part1(state: InfectionStatus) -> int:
    state = defaultdict(bool, state.items())
    infection_count = 0
    current_node = max(n.real for n in state.keys()) // 2 + (min(n.imag for n in state.keys()) // 2)* 1j
    direction = 1j
    for _ in range(10_000):
        node_state = state[current_node]
        direction *= -1j if node_state else 1j
        state[current_node] = not node_state
        current_node += direction
        infection_count += not node_state
    return infection_count


CLEAN = 0
WEAKENED = 1
INFECTED = 2
FLAGGED = 3
STATE_DIRECTIONS = [ 1j, 1, -1j, -1 ]
STATE_TRANSITIONS = [
    WEAKENED,
    INFECTED,
    FLAGGED,
    CLEAN
]
def part2(state: InfectionStatus) -> int:
    quad_state: Dict[complex,int] = \
        defaultdict(lambda: CLEAN,[ (node, INFECTED if value else CLEAN) for node, value in state.items() ])
    current_node = max(n.real for n in state.keys()) // 2 + (min(n.imag for n in state.keys()) // 2)* 1j
    direction = 1j
    infection_count = 0
    for _ in range(10_000_000):
        node_state = quad_state[current_node]
        new_state = STATE_TRANSITIONS[node_state]
        direction *= STATE_DIRECTIONS[node_state]
        quad_state[current_node] = new_state
        current_node += direction
        infection_count += new_state == INFECTED
    return infection_count


def solve(state: InfectionStatus) -> Tuple[int,int]:
    return (
        part1(state),
        part2(state)
    )


def get_input(file_path: str) -> InfectionStatus:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        infection_status: InfectionStatus = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                infection_status[x - y *1j] = c == "#"
        return infection_status


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