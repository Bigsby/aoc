#! /usr/bin/python3

import sys, os, time
import re


class Entry():
    def __init__(self, name, speed, duration, rest):
        self.name = name
        self.speed = int(speed)
        self.duration = int(duration)
        self.rest = int(rest)
        self.period = self.duration + self.rest
        
    def __str__(self):
        return f"{self.name} s:{self.speed} d:{self.duration} r:{self.rest}"
    def __repr__(self):
        return self.__str__()


def calculateDistance(entry, totalDuration):
    period = entry.duration + entry.rest
    periods, remainder = divmod(totalDuration, period)
    total = periods * entry.speed * entry.duration
    remainderTotal = entry.speed if remainder >= entry.duration else entry.speed * (entry.duration - remainder)
    total += remainderTotal
    return total


def part1(puzzleInput):
    totalDuration = 2503
    return max(map(lambda entry: calculateDistance(entry, totalDuration), puzzleInput))


def getDistanceForTime(entry, time):
    timeInPeriod = time % entry.period
    return entry.speed if timeInPeriod < entry.duration else 0


def part2(puzzleInput):
    totalTime = 2503
    deers = { entry.name: { "distance": 0, "points": 0, "entry": entry } for entry in puzzleInput }

    for time in range(0, totalTime):
        maxDistance = 0
        for name in deers:
            deer = deers[name]
            deer["distance"] += getDistanceForTime(deer["entry"], time)
            maxDistance = max(maxDistance, deer["distance"])
        for name in deers:
            if deers[name]["distance"] == maxDistance:
                deers[name]["points"] += 1

    return max(map(lambda name: deers[name]["points"], deers.keys()))


lineRegex = re.compile(r"^(\w+)\scan\sfly\s(\d+)\skm/s\sfor\s(\d+)\sseconds,\sbut\sthen\smust\srest\sfor\s(\d+)\sseconds.$")
def parseLine(line):
    match = lineRegex.match(line)
    return Entry(*match.group(1, 2, 3, 4))


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return [ parseLine(line) for line in file.readlines() ]


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