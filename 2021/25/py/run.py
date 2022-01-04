#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = List[List[str]]
EMPTY = "."

def solve(seafloor: Input) -> Tuple[int,str]:
    step = 0
    width = len(seafloor[0])
    height = len(seafloor)
    while True:
        moved_count = 0
        for cucumber, (x_move, y_move) in [ (">", (1, 0)), ("v", (0, 1)) ]:
            to_move: List[Tuple[int, int, int, int]] = []
            for y in range(height):
                for x in range(width):
                    next_x = (x + x_move) % width
                    next_y = (y + y_move) % height
                    if seafloor[y][x] == cucumber and seafloor[next_y][next_x] == EMPTY:
                        to_move.append((x, y, next_x, next_y))
            for x, y, next_x, next_y in to_move:
                seafloor[y][x] = EMPTY
                seafloor[next_y][next_x] = cucumber
            moved_count += len(to_move)
        if moved_count == 0:
            break
        step += 1
    return (step + 1, "")


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ list(line.strip()) for line in file.readlines() ]


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
