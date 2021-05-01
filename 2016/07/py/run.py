#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple
import re

abba_regex = re.compile(r"([a-z])((?!\1)[a-z])\2\1")


def supports_TLS(ip: List[str]) -> bool:
    return not any(abba_regex.search(hypernet) for hypernet in ip[1::2]) \
        and any(abba_regex.search(supernet) for supernet in ip[::2])


def supports_SSL(ip: List[str]) -> bool:
    abas: Set[Tuple[str, str]] = set()
    babs: Set[Tuple[str, str]] = set()
    for (hyper, part) in enumerate(ip):
        for index in range(len(part) - 2):
            if part[index] == part[index + 2] and part[index] != part[index + 1]:
                if hyper % 2 == 0:
                    babs.add((part[index + 1], part[index]))
                else:
                    abas.add((part[index], part[index + 1]))
    for aba in abas:
        if aba in babs:
            return True
    return False


def solve(ips: List[List[str]]) -> Tuple[int, int]:
    return (
        sum(map(supports_TLS, ips)),
        sum(map(supports_SSL, ips))
    )


def get_input(file_path: str) -> List[List[str]]:
    line_regex = re.compile(r"(\[?[a-z]+\]?)")
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return [line_regex.findall(line) for line in file.readlines()]


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
