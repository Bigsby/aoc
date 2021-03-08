#! /usr/bin/python3

import sys
import os
import time
import re
from enum import Enum
from typing import Dict, List, Tuple


class Direction(Enum):
    Increment = "inc"
    Decrement = "dec"


class Operator(Enum):
    Equal = "=="
    NotEqual = "!="
    LessThan = "<"
    GreaterThan = ">"
    LessOrEqual = "<="
    GreatherOrEqual = ">="


Instruction = Tuple[str, str, Direction, int, Operator, int]


def is_condition_valid(source: int, operator: Operator, value: int) -> bool:
    if operator == Operator.Equal:
        return source == value
    if operator == Operator.NotEqual:
        return source != value
    if operator == Operator.LessThan:
        return source < value
    if operator == Operator.GreaterThan:
        return source > value
    if operator == Operator.LessOrEqual:
        return source <= value
    if operator == Operator.GreatherOrEqual:
        return source >= value
    raise Exception("Unknown operator", operator)


def solve(instructions: List[Instruction]) -> Tuple[int, int]:
    memory: Dict[str, int] = {}
    max_value = 0
    for target, source, direction, amount, operator, value in instructions:
        source_value = memory[source] if source in memory else 0
        if not is_condition_valid(source_value, operator, value):
            continue
        if target not in memory:
            memory[target] = 0
        memory[target] += amount * \
            (1 if direction == Direction.Increment else -1)
        max_value = max(max_value, memory[target])
    return (
        max(memory.values()),
        max_value
    )


line_regex = re.compile(
    r"^(?P<target>[a-z]+)\s(?P<direction>inc|dec)\s(?P<amount>-?\d+)\sif\s(?P<source>[a-z]+)\s(?P<operator>==|!=|>=|<=|>|<)\s(?P<value>-?\d+)$")


def parse_line(line: str) -> Instruction:
    match = line_regex.match(line)
    if match:
        return \
            match.group("target"), \
            match.group("source"), \
            Direction(match.group("direction")), \
            int(match.group("amount")), \
            Operator(match.group("operator")), \
            int(match.group("value"))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Instruction]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [parse_line(line) for line in file.readlines()]


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
