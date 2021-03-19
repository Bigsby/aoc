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
    
    def calculate_distance(self, total_duration: int) -> int:
        periods, remainder = divmod(total_duration, self.period)
        total = periods * self.speed * self.duration
        return total + self.speed * min(remainder, self.duration)

    def get_distance_for_time(self, time: int) -> int:
        return self.speed if time % self.period < self.duration else 0


class Deer:
    def __init__(self, entry: Entry) -> None:
        self.entry = entry
        self.distance = 0
        self.points = 0


def part2(entries: List[Entry]) -> int:
    deers = [ Deer(entry) for entry in entries ]
    for time in range(TIME):
        max_distance = 0
        for deer in deers:
            deer.distance += deer.entry.get_distance_for_time(time)
            max_distance = max(max_distance, deer.distance)
        for deer in deers:
            if deer.distance == max_distance:
                deer.points += 1
    return max(map(lambda deer: deer.points, deers))


def solve(entries: List[Entry]) -> Tuple[int,int]:
    return (
        max(map(lambda entry: entry.calculate_distance(TIME), entries)), 
        part2(entries)
    )


line_regex = re.compile(r"^(\w+)\scan\sfly\s(\d+)\skm/s\sfor\s(\d+)\sseconds,\sbut\sthen\smust\srest\sfor\s(\d+)\sseconds.$")
def parse_line(line: str) -> Entry:
    match = line_regex.match(line)
    if match:
        return Entry(*match.group(1, 2, 3, 4))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> List[Entry]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path, "r") as file:
        return [ parse_line(line) for line in file.readlines() ]


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