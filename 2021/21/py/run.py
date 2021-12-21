#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict
from collections import defaultdict

Input = Tuple[int, int]


def part1(puzzle_input: Input) -> int:
    p1, p2 = puzzle_input
    s1 = s2 = offset = turns = 0
    while True:
        p1 = (p1 + (offset % 100) + ((offset + 1) % 100) + ((offset + 2) % 100) + 2) % 10 + 1
        offset = (offset + 3) % 100
        turns = turns + 3
        s1 = s1 + p1
        if s1 >= 1000:
            return s2 * turns
        (p1, p2, s1, s2) = (p2, p1, s2, s1)


SCORES_FREQUENCIES = [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)]
def calculate_next_states(states, p1, p2, s1, s2, occurrences, wins, player_index):
    for (score, frequency) in SCORES_FREQUENCIES:
        new_position = ((p1 + score - 1) % 10) + 1
        new_score = s1 + new_position
        if new_score < 21:
            states[(p2, new_position, s2, new_score)] += occurrences * frequency
        else:
            wins[player_index] += occurrences * frequency


def part2(puzzle_input: Input) -> int:
    p1, p2 = puzzle_input
    states: Dict[Tuple[int, int, int, int], int] = defaultdict(int)
    states[(p1, p2, 0, 0)] = 1
    wins: List[int] = [0, 0]
    player_index = 0
    while states:
        new_states = defaultdict(int)
        for (p1, p2, s1, s2) in states:
            calculate_next_states(new_states, p1, p2, s1, s2, states[(p1, p2, s1, s2)], wins, player_index)
        player_index = 1 - player_index
        states = new_states
    return max(wins)


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        lines = file.read().splitlines()
        return int(lines[0][-1]), int(lines[1][-1])


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
