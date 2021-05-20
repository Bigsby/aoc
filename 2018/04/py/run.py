#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple
import re

DateTime = Tuple[int,int,int,int,int]
LogRecord = Tuple[DateTime,str]
GuardRecord = Tuple[int,Dict[int,int]]


def record_guard_times(guard_record: GuardRecord, last_asleep: int, woke: int) -> GuardRecord:
    total, minutes = guard_record
    for minute in range(last_asleep, woke):
        total += 1
        minutes[minute] += 1
    return total, minutes


shift_start_regex = re.compile(r"^Guard\s#(?P<id>\d+)\sbegins\sshift")
FALL_ASLEEP = "falls asleep"
WAKE_UP = "wakes up"
def build_guard_records(log: List[LogRecord]) -> Dict[int,GuardRecord]:
    log = sorted(log, key=lambda values: values[0])
    guards: Dict[int,GuardRecord] = {}
    guard_id = 0
    guard_asleep = False
    last_asleep = 0
    for (_, _, _, _, minutes), message in log:
        if message == FALL_ASLEEP:
            last_asleep = minutes
            guard_asleep = True
        elif message == WAKE_UP:
            guard_asleep = False
            guards[guard_id] = record_guard_times(guards[guard_id], last_asleep, minutes)
        else:
            match = shift_start_regex.match(message)
            if match:
                if guard_asleep:
                    guards[guard_id] = record_guard_times(guards[guard_id], last_asleep, 60)
                    guard_asleep = False
                guard_id = int(match.group("id"))
                if guard_id not in guards:
                    guards[guard_id] = ( 0, { minute: 0 for minute in range(60) } )
    return guards
        

def part1(guards: Dict[int,GuardRecord]) -> int:
    max_total = 0
    guardId = -1
    for id, (total, _) in guards.items():
        if total > max_total:
            max_total = total
            guardId = id
    max_total = 0
    max_minute = -1
    for minute, total in guards[guardId][1].items():
        if total > max_total:
            max_total = total
            max_minute = minute
    return guardId * max_minute


def part2(guards: Dict[int,GuardRecord]) -> int:
    max_total = 0
    max_minute = -1
    guard_id = 0
    for id, guard_record in guards.items():
        for minute, total in guard_record[1].items():
            if total > max_total:
                max_total = total
                max_minute = minute
                guard_id = id
    return guard_id * max_minute


def solve(guards: Dict[int,GuardRecord]) -> Tuple[int,int]:
    return (
        part1(guards),
        part2(guards)
    )


line_regex = re.compile(r"\[(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})\s(?P<hours>\d{2}):(?P<minutes>\d{2})\]\s(?P<message>.*)$")
def parse_line(line: str) -> LogRecord:
    match = line_regex.match(line)
    if match:
        return \
            (int(match.group("year")), int(match.group("month")), int(match.group("day")), \
            int(match.group("hours")), int(match.group("minutes"))), \
            match.group("message")
    raise Exception("Bad format", line)


def get_input(file_path: str) -> Dict[int,GuardRecord]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return build_guard_records([ parse_line(line) for line in file.readlines() ])


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()