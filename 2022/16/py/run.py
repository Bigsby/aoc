#! /usr/bin/python3

import sys, os, time
from typing import Tuple, Dict, List, Deque
from collections import deque

Input = Dict[str,Tuple[int,List[str]]]


def build_graph(start: str, valves: Input) -> Dict[str,int]:
    paths: Dict[str,int] = {}
    for end, (rate, _) in valves.items():
        if end == start or rate == 0:
            continue
        queue: List[str,List[str],int] = [(start, [], 0)]
        while queue:
            current, visited, length = queue.pop(0)
            if current == end:
                paths[end] = length
                break
            new_visited = [*visited, current]
            for next in valves[current][1]:
                if next in visited:
                    continue
                queue.append((next, new_visited, length + 1))
    return paths


def part1(valves: Input, useful_valves: List[str], graph: Dict[str,Dict[str,int]]) -> int:
    queue: Deque[Tuple[str,List[str], int]] = deque([("AA", ["AA"], 30, 0)])
    max_released = 0
    while queue:
        current, visited, time_left, released = queue.pop()
        for next in useful_valves:
            if next in visited:
                continue

            new_visited = [*visited, next]
            next_distance = graph[current][next]
            if next_distance >= time_left:
                max_released = max(max_released, released)
                continue

            new_time_left = time_left - next_distance - 1
            new_released = released + valves[next][0] * new_time_left
            if len(new_visited) == len(useful_valves):
                max_released = max(max_released, new_released)
                continue

            queue.append((next, new_visited, new_time_left, new_released))
    return max_released


def process_next(distance: int, time_left: int, released: int, next_rate: int) -> Tuple[int,int]:
    if distance + 2 >= time_left:
        return released, time_left
    new_time_left = time_left - distance - 1
    return released + next_rate * new_time_left, new_time_left


def part2(valves: Input, useful_valves: List[str], graph: Dict[str,Dict[str,int]]) -> int:
    queue: Deque[Tuple[str,str,List[str],int,int,int]] = deque([]) # [("AA", "AA", [ "AA" ], 26, 26, 0)]
    for valve in useful_valves:
        if valve == "AA":
            continue
        time = 26 - graph["AA"][valve] - 1
        queue.append((valve, "AA", ["AA", valve], time, 26, valves[valve][0] * time))
    useful_length = len(useful_valves)
    max_released = 0
    while queue:
        elf, elephant, visited, elf_time_left, elephant_time_left, released = queue.pop()
        for next in useful_valves:
            if next in visited:
                continue
            new_visited = [*visited, next]
            visited_length = len(new_visited)
            next_rate = valves[next][0]
            
            new_released, new_time = process_next(graph[elf][next], elf_time_left, released, next_rate)
            if new_released != released and visited_length < useful_length and new_time > 2:
                queue.append((next, elephant, new_visited, new_time, elephant_time_left, new_released))
            else:
                max_released = max(max_released, new_released)

            new_released, new_time = process_next(graph[elephant][next], elephant_time_left, released, next_rate)
            if new_released != released and visited_length < useful_length and new_time > 2:
                queue.append((elf, next, new_visited, elf_time_left, new_time, new_released))
            else:
                max_released = max(max_released, new_released)

    return max_released
                    

def solve(valves: Input) -> Tuple[int,int]:
    useful_valves = [ valve for valve in valves.keys() if valve == "AA" or valves[valve][0] > 0 ]
    graph: Dict[str,Dict[str,int]] = { valve: build_graph(valve, valves) for valve in useful_valves }
    return (part1(valves, useful_valves, graph), part2(valves, useful_valves, graph))


def process_line(line: str) -> Tuple[str,int,List[str]]:
    splits = line.split()
    return splits[1], int(splits[4].split("=")[1][:-1]), list(map(lambda v: v.strip(","), splits[9:]))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return { valve: (rate, into) for valve, rate, into in map(process_line, file.readlines()) }


def main():
    if len(sys.argv) != 2: raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
