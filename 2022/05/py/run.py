#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict
from collections import defaultdict
import copy

Move = Tuple[int, int, int]
Input = Tuple[Dict[int, List[str]], List[Move]]


def do_moves(puzzle_input: Input, multiple_crates: bool) -> str:
    stacks, moves = puzzle_input
    stacks = copy.deepcopy(stacks)
    for amount, source, target in moves:
        for target_index in range(amount):
            stacks[target].insert(
                target_index if multiple_crates else 0, stacks[source].pop(0))
    return "".join([stacks[key + 1][0] for key in range(len(stacks))])


def solve(puzzle_input: Input) -> Tuple[str, str]:
    return (do_moves(puzzle_input, False), do_moves(puzzle_input, True))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path) as file:
        moves: List[Move] = []
        stacks: Dict[int, List[str]] = defaultdict(list)
        processing_stacks = True
        for line in file.readlines():
            if processing_stacks:
                if line[1] == "1":
                    processing_stacks = False
                    continue
                for index, crate in enumerate(line):
                    if 'A' <= crate <= 'Z':
                        stacks[((index - 1) // 4) + 1].append(crate)
            elif line.strip():
                split = line.strip().split()
                moves.append((int(split[1]), int(split[3]), int(split[5])))
        return (stacks, moves)


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
