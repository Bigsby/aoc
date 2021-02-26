#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re

TIME = 2503


class Entry():
    def __init__(self, name: str, speed:str, duration: str, rest: str):
        self.name = name
        self.speed = int(speed)
        self.duration = int(duration)
        self.rest = int(rest)
        self.period = self.duration + self.rest


class Deer:
    def __init__(self, entry: Entry) -> None:
        self.entry = entry
        self.distance = 0
        self.points = 0


def calculateDistance(entry: Entry, totalDuration: int) -> int:
    periods, remainder = divmod(totalDuration, entry.period)
    total = periods * entry.speed * entry.duration
    return total + entry.speed * min(remainder, entry.duration)


def getDistanceForTime(entry: Entry, time: int) -> int:
    timeInPeriod = time % entry.period
    return entry.speed if timeInPeriod < entry.duration else 0


def part2(entries: List[Entry]) -> int:
    deers = [ Deer(entry) for entry in entries ]
    for time in range(TIME):
        maxDistance = 0
        for deer in deers:
            deer.distance += getDistanceForTime(deer.entry, time)
            maxDistance = max(maxDistance, deer.distance)
        for deer in deers:
            if deer.distance == maxDistance:
                deer.points += 1
    return max(map(lambda deer: deer.points, deers))


def solve(entries: List[Entry]) -> Tuple[int,int]:
    return (
        max(map(lambda entry: calculateDistance(entry, TIME), entries)), 
        part2(entries)
    )


lineRegex = re.compile(r"^(\w+)\scan\sfly\s(\d+)\skm/s\sfor\s(\d+)\sseconds,\sbut\sthen\smust\srest\sfor\s(\d+)\sseconds.$")
def parseLine(line: str) -> Entry:
    match = lineRegex.match(line)
    if match:
        return Entry(*match.group(1, 2, 3, 4))
    raise Exception("Bad format", line)


def getInput(filePath: str) -> List[Entry]:
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