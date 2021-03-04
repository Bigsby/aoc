#! /usr/bin/python3

import sys, os, time
from typing import Callable, List, Tuple


def do_jumps(jumps: List[int], new_jump_junc: Callable[[int],int]) -> int:
    jumps = list(jumps)
    max_index = len(jumps)
    index = 0
    count = 0
    while index >= 0 and index < max_index:
        count += 1
        offset = jumps[index]
        next_index = index + offset
        jumps[index] = offset + new_jump_junc(offset)
        index = next_index
    return count


def solve(jumps: List[int]) -> Tuple[int,int]:
    return (
        do_jumps(jumps, lambda _: 1),
        do_jumps(jumps, lambda offset: 1 if offset < 3 else -1)
    )


def get_input(file_path: str) -> List[int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ int(line) for line in file.readlines() ]


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