#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
from functools import reduce


def get_column_records(messages: List[str]) -> Dict[int, Dict[str, int]]:
    column_records: Dict[int, Dict[str, int]] = {i: {} for i in range(len(messages[0]))}
    for message in messages:
        for column, c in enumerate(message):
            if c in column_records[column]:
                column_records[column][c] += 1
            else:
                column_records[column][c] = 1
    return column_records


def solve(messages: List[str]) -> Tuple[str, str]:
    column_records = get_column_records(messages)
    return (
        reduce(lambda soFar, column: soFar + max(column_records[column].items(
        ), key=lambda cr: cr[1])[0], range(len(messages[0])), ""),
        reduce(lambda soFar, column: soFar + min(column_records[column].items(
        ), key=lambda cr: cr[1])[0], range(len(messages[0])), "")
    )


def get_input(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [line.strip() for line in file.readlines()]


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
