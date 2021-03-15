#! /usr/bin/python3

import sys
import os
import time
from typing import Any, Dict, List, Tuple, Union
import re
import json

JSONType = Union[str, int, float, bool, None, Dict[str, Any], List[Any]]


def get_total(obj: JSONType) -> int:
    if isinstance(obj, dict):
        if any(filter(lambda value: value == "red", obj.values())):
            return 0
        return sum(get_total(value) for value in obj.values())
    if isinstance(obj, int):
        return int(obj)
    if isinstance(obj, list):
        return sum(get_total(item) for item in obj)
    return 0


def solve(puzzle_input: str) -> Tuple[int, int]:
    number_regex = re.compile(r"(-?[\d]+)")
    return (
        sum(int(match.group(1))
            for match in number_regex.finditer(puzzle_input)),
        get_total(json.loads(puzzle_input))
    )


def get_input(file_path: str) -> str:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.read().strip()


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
