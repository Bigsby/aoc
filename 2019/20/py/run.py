#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple, Set

Position = complex
LevelPosition = Tuple[Position, int]
Maze = List[Position]
Portals = Dict[Position, str]
DIRECTIONS = [1j, -1j, 1, -1]


def part1(data: Tuple[Maze, Portals, Position, Position]) -> int:
    maze, portals, start, end = data
    visited = {start}
    queue: List[Tuple[Position, int]] = [(start, 1)]
    while queue:
        position, distance = queue.pop(0)
        new_positions: List[Position] = []
        if position in portals:
            new_positions.append(next(p for p, label in portals.items(
            ) if label == portals[position] and p != position))
        for direction in DIRECTIONS:
            new_positions.append(position + direction)
        for new_position in new_positions:
            if new_position == end:
                return distance
            if new_position not in visited and new_position in maze:
                visited.add(new_position)
                queue.append((new_position, distance + 1))
    raise Exception("Path not found")


def part2(data: Tuple[Maze, Portals, Position, Position]) -> int:
    maze, portals, start, end = data
    min_x = min(p.real for p in maze)
    max_x = max(p.real for p in maze)
    min_y = min(p.imag for p in maze)
    max_y = max(p.imag for p in maze)
    outer_portals = {position: label for position, label in portals.items()
                    if position.real == min_x or position.real == max_x or
                    position.imag == min_y or position.imag == max_y}
    inner_portals = {position: label for position,
                    label in portals.items() if position not in outer_portals}
    reverse_outer_portals = {label: position for position,
                           label in outer_portals.items()}
    reverse_inner_portals = {label: position for position,
                           label in inner_portals.items()}
    end_position = (end, 0)
    start_position = (start, 0)
    visited: Set[LevelPosition] = {start_position}
    queue: List[Tuple[int, float, float, int]] = [
        (1, start_position[0].real, start_position[0].imag, start_position[1])]
    while queue:
        distance, x, y, level = queue.pop(0)
        position = x + y * 1j
        new_positions: List[LevelPosition] = []
        if position in inner_portals:
            new_positions.append(
                (reverse_outer_portals[inner_portals[position]], level + 1))
        elif level != 0 and position in outer_portals:
            new_positions.append(
                (reverse_inner_portals[outer_portals[position]], level - 1))
        for direction in DIRECTIONS:
            new_positions.append((position + direction, level))
        for new_position in new_positions:
            if new_position == end_position:
                return distance
            if new_position not in visited and new_position[0] in maze:
                visited.add(new_position)
                queue.append(
                    (distance + 1, new_position[0].real, new_position[0].imag, new_position[1]))
    raise Exception("Path not found")


def solve(data: Tuple[Maze, Portals, Position, Position]) -> Tuple[int, int]:
    return (
        part1(data),
        part2(data)
    )


def get_input(file_path: str) -> Tuple[Maze, Portals, Position, Position]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        maze: Maze = []
        portals: Portals = {}
        start = 0j
        end = 0j
        lines = file.readlines()
        for y, line in enumerate(lines):
            for x, c in enumerate(line):
                position = x + y * 1j
                if c == ".":
                    maze.append(position)
                    portal = ""
                    if lines[y - 1][x].isalpha():
                        portal = lines[y - 2][x] + lines[y - 1][x]
                    elif lines[y + 1][x].isalpha():
                        portal = lines[y + 1][x] + lines[y + 2][x]
                    elif line[x - 1].isalpha():
                        portal = lines[y][x - 2] + line[x - 1]
                    elif line[x + 1].isalpha():
                        portal = line[x + 1] + line[x + 2]
                    if portal:
                        if portal == "AA":
                            start = position
                        elif portal == "ZZ":
                            end = position
                        else:
                            portals[position] = portal

        return maze, portals, start, end


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
