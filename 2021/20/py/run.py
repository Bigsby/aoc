#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List, Dict

Image = Dict[Tuple[int, int], bool]
Input = Tuple[List[bool], Image, int, int]


def get_pixel_value(pixel_x: int, pixel_y: int, image: Image, default: bool) -> int:
    pixel_value = 0
    for (x_offset,y_offset) in [(-1,-1),(0,-1),(1,-1),(-1,0),(0,0),(1,0),(-1,1),(0,1),(1,1)]:
        pixel_value = (pixel_value << 1) + image.get((pixel_x + x_offset, pixel_y + y_offset), default)
    return pixel_value


def run_algorithm(image: Image, algorithm: List[bool], step: int, max_x: int, max_y: int) -> Tuple[Image, int]:
    default = algorithm[0] if step % 2 else algorithm[-1]
    overflow = step + 1
    new_image: Image = {} 
    lit_count = 0
    for x in range(-overflow, max_x + overflow):
        for y in range(-overflow, max_y + overflow):
            lit = algorithm[get_pixel_value(x, y, image, default)]
            lit_count += lit
            new_image[(x, y)] = lit
    return new_image, lit_count


def solve(puzzle_input: Input) -> Tuple[int,int]:
    algorithm, image, max_x, max_y = puzzle_input
    lit_count = 0
    part1 = 0
    for step in range(50):
        image, lit_count = run_algorithm(image, algorithm, step, max_x, max_y)
        if step == 1:
            part1 = lit_count
    return (part1, lit_count)


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        algorithm_line = file.readline().strip()
        algorithm = [ c == '#' for c in algorithm_line ]
        file.readline()
        x = 0
        y = 0
        max_x = 0
        image: Image = {}
        for line in file.readlines():
            for c in line.strip():
                image[(x, y)] = c == '#'
                x += 1
            max_x = x
            y += 1
            x = 0
        return algorithm, image, max_x, y


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
