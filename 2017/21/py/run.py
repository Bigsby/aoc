#! /usr/bin/python3

import sys
import os
import time
import re
from typing import Dict, Iterable, List, Set, Tuple

Position = complex
Grid = Set[Position]
Rule = Tuple[Grid, Grid]
Rules = Dict[int, List[Rule]]
START = ".#./..#/###"


def print_grid(grid: Grid):
    max_x = int(max(p.real for p in grid))
    max_y = int(max(p.imag for p in grid))
    for y in range(max_y + 1):
        for x in range(max_x + 1):
            print("#" if x + y * 1j in grid else ".", end="")
        print()
    print()


def parse_grid(text: str) -> Tuple[int, Grid]:
    grid: Grid = set()
    split = text.split("/")
    for y, line in enumerate(split):
        for x, c in enumerate(line):
            if c == "#":
                grid.add(x + y * 1j)
    return len(split[0]), grid


def mirror_horizontal(grid: Grid, size: int) -> Grid:
    return {position.imag * 1j + size - 1 - position.real for position in grid}


def rotate_clockwise(grid: Grid, size: int) -> Grid:
    return {position.real * 1j + size - 1 - position.imag for position in grid}


def generate_permutations(grid: Grid, size: int) -> Iterable[Grid]:
    for _ in range(4):
        yield grid
        yield mirror_horizontal(grid, size)
        grid = rotate_clockwise(grid, size)


def enhance_grid(grid: Grid, size: int, rules: List[Rule]) -> Grid:
    for permutation in generate_permutations(grid, size):
        for match, result in rules:
            if match == permutation:
                return result
    raise Exception("Rule not found")


def split_grid(grid: Grid, count: int, size: int) -> Iterable[Tuple[int, int, Grid]]:
    for y_index in range(count):
        for x_index in range(count):
            x_offset = x_index * size
            y_offset = y_index * size
            inner_grid = {
                p - (x_index * size) - (y_index * size) * 1j
                for p in grid
                if x_offset <= p.real < x_offset + size and y_offset <= p.imag < y_offset + size}
            yield x_index, y_index, inner_grid


def iterate(grid: Grid, size: int, rules: Rules) -> Tuple[int, Grid]:
    enhanced_grid: Grid = set()
    divider = 0
    rule_size = 0
    if size % 2 == 0:
        rule_size = 2
    elif size % 3 == 0:
        rule_size = 3
    rule_set = rules[rule_size]
    divider = size // rule_size
    for x_index, y_index, inner_grid in split_grid(grid, divider, rule_size):
        for position in enhance_grid(inner_grid, rule_size, rule_set):
            enhanced_grid.add(position + x_index * (rule_size +
                                                    1) + y_index * 1j * (rule_size + 1))
    return size + divider, enhanced_grid


def run_iterations(grid: Grid, size: int, rules: Rules, iterations: int) -> Tuple[int, Grid]:
    for _ in range(iterations):
        size, grid = iterate(grid, size, rules)
    return size, grid


def run_next_3_Iterations(grid: Grid, rules: Rules) -> List[Grid]:
    _, grid = run_iterations(grid, 3, rules, 3)
    return [innerGrid for _, _, innerGrid in split_grid(grid, 3, 3)]


def get_grid_id(grid: Grid) -> int:
    result = 0
    for y in range(3):
        for x in range(3):
            if x + y * 1j in grid:
                result += (1 << x) << 3 * y
    return result


def part2(rules: Rules, grid: Grid) -> int:
    total = 0
    calculated: Dict[int, List[Grid]] = {}
    queue: List[Tuple[Grid, int]] = [(grid, 0)]
    while queue:
        grid, iterations = queue.pop()
        if iterations == 18:
            total += len(grid)
        else:
            grid_id = get_grid_id(grid)
            if grid_id not in calculated:
                calculated[grid_id] = run_next_3_Iterations(grid, rules)
            for inner_grid in calculated[grid_id]:
                queue.append((inner_grid, iterations + 3))
    return total


def solve(rules: Rules) -> Tuple[int, int]:
    size, grid = parse_grid(START)
    return (
        len(run_iterations(grid, size, rules, 5)[1]),
        part2(rules, grid)
    )


line_regex = re.compile(r"^(?P<rule>[./#]+) => (?P<result>[./#]+)$")


def parse_line(line: str) -> Tuple[int, Rule]:
    match = line_regex.match(line)
    if match:
        rule_size, rule_grid = parse_grid(match.group("rule"))
        _, result_grid = parse_grid(match.group("result"))
        return rule_size, (rule_grid, result_grid)
    raise Exception("Bad format", line)


def get_input(file_path: str) -> Dict[int, List[Rule]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        rules: Dict[int, List[Rule]] = {2: [], 3: []}
        for line in file.readlines():
            size, rule = parse_line(line)
            rules[size].append(rule)
        return rules


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
