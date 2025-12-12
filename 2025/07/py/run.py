#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Set

Input = Tuple[complex,Set[complex]]

def part1(puzzle_input: Input) -> int:
    start, splitters = puzzle_input
    max_y = int(max(s.imag for s in splitters)) + 1
    beams = [ start ]
    visited = set(beams)
    splits = set() 
    while beams:
        beam = beams.pop()
        while beam.imag < max_y:
            beam += 1j
            if beam in visited:
                break
            visited.add(beam)
            if beam in splitters:
                splits.add(beam)
                beams.append(beam + 1)
                beams.append(beam - 1)
                break
    return len(splits)


def part2(puzzle_input: Input) -> int:
    return 2


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (part1(puzzle_input), part2(puzzle_input))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        start = 0
        splitters = set() 
        for row, line in enumerate(file.readlines()):
            for column, c in enumerate(line.strip()):
                if c == 'S':
                    start = column + row * 1j
                elif c == '^':
                    splitters.add(column + row * 1j)
        return start, splitters


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
