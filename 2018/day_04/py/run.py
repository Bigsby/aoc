#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re

Date = Tuple[int,int,int]
Time = Tuple[int,int]
LogRecord = Tuple[Date,Time,str]
GuardRecord = Tuple[int,Dict[int,int]]


def recordGuardTimes(id: int, guards: Dict[int,GuardRecord], lastAsleep: int, woke: int) -> GuardRecord:
    if id not in guards:
        guards[id] = ( 0, { minute: 0 for minute in range(60) } )
    guardRecord = guards[id]
    total, minutes = guardRecord
    for minute in range(lastAsleep, woke):
        total += 1
        minutes[minute] += 1
    return total, minutes


shiftStartRegex = re.compile(r"^Guard\s#(?P<id>\d+)\sbegins\sshift")
FALL_ASLEEP = "falls asleep"
WAKE_UP = "wakes up"
def buildGuardRecords(log: List[LogRecord]) -> Dict[int,GuardRecord]:
    log = sorted(log, key=lambda values: (values[0], values[1]))
    guards: Dict[int,GuardRecord] = {}
    guardId = 0
    guardAsleep = False
    lastAsleep = 0
    for _, (_, minutes), message in log:
        match = shiftStartRegex.match(message)
        if match:
            if guardAsleep:
                guards[guardId] = recordGuardTimes(guardId, guards, lastAsleep, 60)
                guardAsleep = False
            guardId = int(match.group("id"))
            continue
        if message == FALL_ASLEEP:
            lastAsleep = minutes
            guardAsleep = True
        if message == WAKE_UP:
            guardAsleep = False
            guards[guardId] = recordGuardTimes(guardId, guards, lastAsleep, minutes)
    return guards
        

def part1(guards: Dict[int,GuardRecord]) -> int:
    maxTotal = 0
    guardId = -1
    for id, guardRecord in guards.items():
        total, _ = guardRecord
        if total > maxTotal:
            maxTotal = total
            guardId = id
    maxTotal = 0
    maxMinute = -1
    for minute, total in guards[guardId][1].items():
        if total > maxTotal:
            maxTotal = total
            maxMinute = minute
    return guardId * maxMinute


def part2(guards: Dict[int,GuardRecord]) -> int:
    maxTotal = 0
    maxMinute = -1
    guardId = 0
    for id, guardRecord in guards.items():
        for minute, total in guardRecord[1].items():
            if total > maxTotal:
                maxTotal = total
                maxMinute = minute
                guardId = id
    return guardId * maxMinute


lineRegex = re.compile(r"\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2})\]\s(?P<message>.*)$")
def parseLine(line: str) -> LogRecord:
    match = lineRegex.match(line)
    if match:
        return (int(match.group("year")), int(match.group("month")), int(match.group("day"))), \
                (int(match.group("hours")), int(match.group("minutes"))), \
                match.group("message")
    raise Exception("Bad format", line)


def getInput(filePath: str) -> Dict[int,GuardRecord]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return buildGuardRecords([ parseLine(line) for line in file.readlines() ])


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