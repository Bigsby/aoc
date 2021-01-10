#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

Group = Tuple[int,Dict[str,int]]


def countGroupAnswers(group: Group) -> int:
    _, record = group
    return sum(map(lambda letter: record[letter] != 0, record.keys()))


def part1(groups: List[Group]) -> int:
    return sum(map(lambda group: countGroupAnswers(group), groups))


def getGroupCommonAnswers(group: Group) -> int:
    peopleCount, record = group
    return sum(map(lambda letter: record[letter] == peopleCount, record.keys()))


def part2(groups: List[Group]) -> int:
    return sum(map(lambda group: getGroupCommonAnswers(group), groups))


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