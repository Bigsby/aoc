#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Component = Tuple[int,int]


def findStrongest(components: List[Component], lengthMatters: bool) -> int:
    starts = [ component for component in components if 0 in component ]
    queue: List[Tuple[int,int,List[Component]]] = [ (next(port for port in start if port != 0), 0, [start]) for start in starts ]
    longestStrongest = (0, 0)
    while queue:
        lastPort, strength, used = queue.pop(0)
        continued = False
        for component in components:
            if lastPort in component and component not in used:
                continued = True
                nextPort = lastPort if component[0] == component[1] else next(port for port in component if port != lastPort)
                newUsed = used[:]
                newUsed.append(component)
                queue.append((nextPort, strength + lastPort * 2, newUsed))
        if not continued:
            length = len(used) if lengthMatters else 0
            longestStrongest = max(longestStrongest, (length, strength + lastPort))
    return longestStrongest[1]


def part1(components: List[Component]) -> int:
    return findStrongest(components, False)


def part2(components: List[Component]) -> int:
    return findStrongest(components, True)


def getInput(filePath: str) -> List[Component]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ tuple(map(int, re.findall(r"\d+", line))) for line in file.readlines() ]
            



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
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()