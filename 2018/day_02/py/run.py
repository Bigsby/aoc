#! /usr/bin/python3

import sys, os, time
from typing import List
from itertools import combinations


def part1(ids: List[str]) -> int:
    twiceCount = 0
    thriceCount = 0
    for id in ids:
        idCounts = { id.count(c) for c in id }
        twiceCount += 2 in idCounts
        thriceCount += 3 in idCounts
    return twiceCount * thriceCount
    

def part2(ids: List[str]) -> str:
    for id1, id2 in combinations(ids, 2):
        differences = [ i for i in range(len(id1)) if id1[i] != id2[i] ]
        if len(differences) == 1:
            diferentIndex = differences[0]
            return id1[:diferentIndex] + id1[diferentIndex + 1:]
    raise Exception("Ids differencing 1 not found")


def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip() for line in file.readlines() ]


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