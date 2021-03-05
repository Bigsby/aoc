#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple

Group = Tuple[int, List[int]]


def get_group_common_answers(group: Group) -> int:
    people_count, answers = group
    return len(list(filter(lambda count: count == people_count, answers)))


def solve(groups: List[Group]) -> Tuple[int, int]:
    return (
        sum(map(lambda group: len(group[1]), groups)),
        sum(map(lambda group: get_group_common_answers(group), groups))
    )


def process_entry(entry: str) -> Group:
    record: Dict[str, int] = {}
    people_count = 0
    for line in entry.split("\n"):
        if line:
            people_count += 1
        for c in line:
            if c in record:
                record[c] += 1
            else:
                record[c] = 1
    return (people_count, list(record.values()))


def get_input(file_path: str) -> List[Group]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [process_entry(entry) for entry in file.read().split("\n\n")]


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
