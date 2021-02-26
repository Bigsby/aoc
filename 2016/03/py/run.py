#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

TriangleSides = List[List[int]]


def isPossibleTriangle(sideA: int, sideB: int, sideC: int) -> bool:
    return sideA < (sideB + sideC) \
            and sideB < (sideA + sideC) \
            and sideC < (sideA + sideB)


def solve(triangleSides: TriangleSides) -> Tuple[int,int]:
    return (
        sum([ isPossibleTriangle(sideA, sideB, sideC) for sideA, sideB, sideC in triangleSides ]), 
        sum(map(lambda index: isPossibleTriangle(\
                triangleSides[(index // 3) * 3][index % 3], \
                triangleSides[(index // 3) * 3 + 1][index % 3], \
                triangleSides[(index // 3) * 3 + 2][index % 3]), \
                range(len(triangleSides))
        ))
    )


lineRegex = re.compile(r"\d+")
def parseLine(line: str) -> List[int]:
    return [ int(i) for i in  lineRegex.findall(line) ]


def getInput(filePath: str) -> List[List[int]]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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