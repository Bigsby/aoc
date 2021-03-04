#! /usr/bin/python3

import sys, os, time
from typing import Tuple
from collections import Counter


def is_password_valid(password: str, check2: bool) -> bool:
    if "".join(list(sorted(list(password)))) == password:
        counts = Counter(password).values()
        return (not check2 or 2 in counts) and any(count > 1 for count in counts)
    return False


def get_valid_password_count(limits: Tuple[int,int], check2: bool) -> int:
    start, end = limits
    return sum([ is_password_valid(str(password), check2) for password in range(start, end) ])


def solve(limits: Tuple[int,int]) -> Tuple[int,int]:
    return (
        get_valid_password_count(limits, False),
        get_valid_password_count(limits, True)
    )


def get_input(file_path: str) -> Tuple[int,int]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        split = file.read().split("-")
        return (int(split[0]), int(split[1]))


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