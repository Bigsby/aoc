#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

Group = Tuple[int,Dict[str,int]]


def getGroupCommonAnswers(group: Group) -> int:
    peopleCount, record = group
    return sum(map(lambda letter: record[letter] == peopleCount, record.keys()))


def solve(groups: List[Group]) -> Tuple[int,int]:
    return (
        sum(map(lambda group: len(group[1]), groups)),
        sum(map(lambda group: getGroupCommonAnswers(group), groups))
    )


def processEntry(entry: str) -> Group:
    record: Dict[str,int] = {}
    peopleCount = 0
    for line in entry.split("\n"):
        if line:
            peopleCount = peopleCount + 1
        for c in line:
            if c in record:
                record[c] += 1
            else:
                record[c] = 1
    return (peopleCount, record)


def getInput(filePath: str) -> List[Group]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ processEntry(entry) for entry in file.read().split("\n\n") ]


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