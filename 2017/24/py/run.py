#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Component = Tuple[int,int]


def solve(components: List[Component]) -> Tuple[int,int]:
    starts = [ component for component in components if 0 in component ]
    queue: List[Tuple[int,int,List[Component]]] = [ (next(port for port in start if port != 0), 0, [start]) 
        for start in starts ]
    longestStrongest1 = (0, 0)
    longestStrongest2 = (0, 0)
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
            longestStrongest1 = max(longestStrongest1, (0, strength + lastPort))
            longestStrongest2 = max(longestStrongest2, (len(used), strength + lastPort))
    return longestStrongest1[1], longestStrongest2[1]


def getInput(filePath: str) -> List[Component]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ tuple(map(int, re.findall(r"\d+", line))) for line in file.readlines() ]


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