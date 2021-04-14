#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple
import re

Operation = Tuple[str, int, int, int]


MASK = 16777215
MULTIPLIER = 65899


def solve(data: Tuple[int, List[Operation]]) -> Tuple[int, int]:
    _, operations = data
    magic_number = operations[7][1]
    part1_result = 0
    seen: Set[int] = set()
    result = 0
    last_result = -1
    while True:
        accumulator = result | 0x10000
        result = magic_number
        while True:
            result = (((result + (accumulator & 0xFF)) & MASK)
                      * MULTIPLIER) & MASK
            if accumulator <= 0xFF:
                if part1_result == 0:
                    part1_result = result
                else:
                    if result not in seen:
                        seen.add(result)
                        last_result = result
                        break
                    else:
                        return part1_result, last_result
            else:
                accumulator //= 0x100


operation_regex = re.compile(
    r"^(?P<mnemonic>\w+) (?P<A>\d+) (?P<B>\d+) (?P<C>\d+)$")


def get_input(filePath: str) -> Tuple[int, List[Operation]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        lines = file.readlines()
        ip = int(lines[0].split(" ")[1])
        operations: List[Operation] = []
        for line in lines[1:]:
            match = operation_regex.match(line)
            if match:
                operations.append((match.group("mnemonic"), int(
                    match.group("A")), int(match.group("B")), int(match.group("C"))))
        return ip, operations


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
