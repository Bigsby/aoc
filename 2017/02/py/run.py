#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re
from itertools import permutations


def solve(lines: List[List[int]]) -> Tuple[int,int]:
    total1 = 0
    total2 = 0
    for line in lines:
        total1 += max(line) - min(line)
        for numberA, numberB in permutations(line, 2):
            if numberA > numberB and numberA % numberB == 0:
                total2 += numberA // numberB
    return (total1, total2)


lineRegex = re.compile(r"\d+")
def getInput(filePath: str) -> List[List[int]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ [ int(i) for i in lineRegex.findall(line) ] for line in file.readlines() ]


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()