#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Dict

Input = Dict[complex,int]
DIRECTIONS = [-1, -1j, 1, 1j]

def is_visible(trees: Input, x_max: int, y_max: int, tree: complex, direction: complex) -> bool:
    tree_height = trees[tree]
    test = tree + direction
    while 0 <= test.real <= x_max and 0 <= test.imag <= y_max:
        if trees[test] >= tree_height:
            return False
        test += direction
    return True


def part1(trees: Input, x_max: int, y_max: int) -> int:
    visible_trees = 2 * x_max + 2 * y_max
    for x, y in ((x, y) for x in range(1, x_max) for y in range(1, y_max)):
        for direction in DIRECTIONS:
            if is_visible(trees, x_max, y_max, x + y * 1j, direction):
                visible_trees += 1
                break
    return visible_trees


def get_scenic_score(trees: Input, x_max: int, y_max: int, tree: complex) -> int:
    scenic_score = 1
    tree_height = trees[tree]
    for direction in DIRECTIONS:
        test = tree + direction
        direction_score = 0
        while 0 <= test.real <= x_max and 0 <= test.imag <= y_max:
            direction_score += 1
            if trees[test] >= tree_height:
                break
            test += direction
        scenic_score *= direction_score
    return scenic_score


def part2(trees: Input, x_max: int, y_max: int) -> int:
    max_scenic_score = 0
    for x, y in ((x, y) for x in range(1, x_max) for y in range(1, y_max)):
        max_scenic_score = max(max_scenic_score, get_scenic_score(trees, x_max, y_max, x + y * 1j))
    return max_scenic_score


def solve(trees: Input) -> Tuple[int,int]:
    x_max = int(max(map(lambda tree: tree.real, trees)))
    y_max = int(max(map(lambda tree: tree.imag, trees)))
    return (part1(trees, x_max, y_max), part2(trees, x_max, y_max))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        tree = 0j
        trees: Input = {}
        for line in file.readlines():
            for c in line.strip():
                trees[tree] = int(c)
                tree += 1
            tree = (tree.imag + 1) * 1j
        return trees


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
