#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

Component = Tuple[int,int]


def solve(components: List[Component]) -> Tuple[int,int]:
    starts = [ component for component in components if 0 in component ]
    queue: List[Tuple[int,int,List[Component]]] = [ (next(port for port in start if port != 0), 0, [start]) 
        for start in starts ]
    longest_strongest_1 = (0, 0)
    longest_strongest_2 = (0, 0)
    while queue:
        last_port, strength, used = queue.pop(0)
        continued = False
        for component in components:
            if last_port in component and component not in used:
                continued = True
                nextPort = last_port if component[0] == component[1] else next(port for port in component if port != last_port)
                newUsed = used[:]
                newUsed.append(component)
                queue.append((nextPort, strength + last_port * 2, newUsed))
        if not continued:
            longest_strongest_1 = max(longest_strongest_1, (0, strength + last_port))
            longest_strongest_2 = max(longest_strongest_2, (len(used), strength + last_port))
    return longest_strongest_1[1], longest_strongest_2[1]


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