#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple
import re
from functools import reduce
from itertools import product


abba_regex = re.compile(r"([a-z])((?!\1)[a-z])\2\1")
def supports_TLS(ip: List[str]) -> bool:
    return not any(abba_regex.search(hypernet) for hypernet in ip[1::2]) \
        and any(abba_regex.search(supernet) for supernet in ip[::2])


def find_BABs(supernet: str) -> Set[str]:
    return {"".join([supernet[i+1], supernet[i], supernet[i+1]])
            for i in range(len(supernet) - 2)
            if supernet[i] == supernet[i + 2]}


def supports_SSL(ip: List[str]) -> bool:
    babs: Set[str] = reduce(lambda soFar, supernet: soFar |
                            find_BABs(supernet), ip[::2], set())
    return any(bab in hypernet for bab, hypernet in product(babs, ip[1::2]))


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
