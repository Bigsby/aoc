#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
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


def solve(ids: List[str]) -> Tuple[int,str]:
    return (
        part1(ids),
        part2(ids)
    )


def getInput(filePath: str) -> List[str]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ line.strip() for line in file.readlines() ]


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