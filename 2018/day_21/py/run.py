#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Operation = Tuple[str,int,int,int]
MASK = 16777215
MULTIPLIER = 65899


def findNumber(magicNumber: int, firstResult: bool = True) -> int:
    seen = set()
    result = 0
    lastResult = -1
    while True:
        accumulator = result | 0x10000
        result = magicNumber
        while True:
            result = (((result + (accumulator & 0xFF)) & MASK) * MULTIPLIER) & MASK
            if accumulator <= 0xFF:
                if firstResult:
                    return result
                else:
                    if result not in seen:
                        seen.add(result)
                        lastResult = result
                        break
                    else:
                        return lastResult
            else:
                accumulator //= 0x100


def part1(data: Tuple[int,List[Operation]]) -> int:
    _, operations = data
    return findNumber(operations[7][1], True)


def part2(data: Tuple[int,List[Operation]]) -> int:
    _, operations = data
    return findNumber(operations[7][1], False)


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