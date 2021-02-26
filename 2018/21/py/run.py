#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Operation = Tuple[str,int,int,int]


MASK = 16777215
MULTIPLIER = 65899
def solve(data: Tuple[int,List[Operation]]) -> Tuple[int,int]:
    _, operations = data
    magicNumber = operations[7][1]
    part1Result = 0
    seen = set()
    result = 0
    lastResult = -1
    while True:
        accumulator = result | 0x10000
        result = magicNumber
        while True:
            result = (((result + (accumulator & 0xFF)) & MASK) * MULTIPLIER) & MASK
            if accumulator <= 0xFF:
                if part1Result == 0:
                    part1Result = result
                else:
                    if result not in seen:
                        seen.add(result)
                        lastResult = result
                        break
                    else:
                        return part1Result, lastResult
            else:
                accumulator //= 0x100


operationRegex = re.compile(r"^(?P<mnemonic>\w+) (?P<A>\d+) (?P<B>\d+) (?P<C>\d+)$")
def getInput(filePath: str) -> Tuple[int,List[Operation]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        lines = file.readlines()
        ip = int(lines[0].split(" ")[1])
        operations = []
        for line in lines[1:]:
            match = operationRegex.match(line)
            if match:
                operations.append((match.group("mnemonic"), int(match.group("A")), int(match.group("B")), int(match.group("C"))))
        return ip, operations


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