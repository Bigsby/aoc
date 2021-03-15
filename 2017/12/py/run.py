#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple
import re


def get_program_group(program: int, connections: Dict[int, List[int]]) -> Set[int]:
    queue = [program]
    result = {program}
    while queue:
        for connection in connections[queue.pop()]:
            if connection not in result:
                queue.append(connection)
                result.add(connection)
    return result


def solve(connections: Dict[int, List[int]]) -> Tuple[int, int]:
    part1_result = len(get_program_group(0, connections))
    groups_count = 0
    while connections:
        groups_count += 1
        for connection in get_program_group(next(iter(connections.keys())), connections):
            if connection in connections:
                del connections[connection]
    return part1_result, groups_count


line_regex = re.compile(r"^(?P<one>\d+)\s<->\s(?P<two>.*)$")


def parse_line(line: str) -> Tuple[int, List[int]]:
    match = line_regex.match(line)
    if match:
        return int(match.group("one")), list(map(int, match.group("two").split(",")))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> Dict[int, List[int]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return {program: connections for program, connections in [parse_line(line) for line in file.readlines()]}


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
