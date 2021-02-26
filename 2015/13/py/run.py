#! /usr/bin/python3

import sys, os, time
import re
from itertools import permutations
from typing import Dict, Iterable, List, Tuple

Entries = Dict[str,Dict[str,int]]


def calculateHappiness(arrangement: Tuple[str,...], entries: Entries) -> int:
    total = 0
    length = len(arrangement)
    for index, person in enumerate(arrangement):
        total += entries[person][arrangement[index - 1]]
        total += entries[person][arrangement[index + 1 if index < length - 1 else 0]]
    return total


def calculateMaximumHappiness(possibleArragements: Iterable[Tuple[str,...]], entries: Entries) -> int:
    return max(map(lambda arrangement: calculateHappiness(arrangement, entries), possibleArragements))


def getPossibleArrangements(people: List[str]) -> Iterable[Tuple[str,...]]:
    return permutations(people, len(people))


def part1(entries: Entries) -> int:
    possibleArragements = getPossibleArrangements(list(entries.keys()))
    result = calculateMaximumHappiness(possibleArragements, entries)
    return result


def part2(entries: Entries) -> int:
    me = "me"
    entries[me] = {}
    for person in list(entries.keys()):
        if person == me:
            continue
        entries[me][person] = 0
        entries[person][me] = 0
    return part1(entries)


def solve(entries: Entries) -> Tuple[int,int]:
    return (part1(entries), part2(entries))


lineRegex = re.compile(r"^(\w+)\swould\s(gain|lose)\s(\d+)\shappiness\sunits\sby\ssitting\snext\sto\s(\w+)\.$")
def getInput(filePath: str) -> Entries:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        entries = {}
        for line in file.readlines():
            match = lineRegex.match(line)
            if match:
                target = match.group(1)
                if target not in entries:
                    entries[target] = {}
                entries[target][match.group(4)] = (1 if match.group(2) == "gain" else -1) * int(match.group(3))
            else:
                raise Exception("Bad format", line)
        return entries


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