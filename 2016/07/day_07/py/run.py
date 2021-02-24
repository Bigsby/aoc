#! /usr/bin/python3

import sys, os, time
from typing import List, Set
import re
from functools import reduce
from itertools import product


abbaRegex = re.compile(r"([a-z])((?!\1)[a-z])\2\1")
def supportsTLS(ip: List[str]) -> bool:
    if any(abbaRegex.search(hypernet) for hypernet in ip[1::2]):
        return False
    return any(abbaRegex.search(supernet) for supernet in ip[::2])


def part1(ips: List[List[str]]) -> int:
    return sum(map(supportsTLS, ips))


def findBABs(supernet: str) -> Set[str]:
    return { "".join([supernet[i+1], supernet[i], supernet[i+1] ]) \
            for i in range(len(supernet) - 2) \
            if supernet[i] == supernet[i + 2] }


def supportsSSL(ip: List[str]) -> bool:
    babs: Set[str] = reduce(lambda soFar, supernet: soFar | findBABs(supernet), ip[::2], set())
    return any(bab in hypernet for bab, hypernet in product(babs, ip[1::2]))


def part2(ips: List[List[str]]) -> int:
    return sum(map(supportsSSL, ips))


lineRegex = re.compile(r"(\[?[a-z]+\]?)")
def getInput(filePath: str) -> List[List[str]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ lineRegex.findall(line) for line in file.readlines() ]
            


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()