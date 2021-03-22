#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Tuple
import re


def build_dependency_graph(pairs: List[Tuple[str, str]]) -> Dict[str, List[str]]:
    dependencies: Dict[str, List[str]] = {}
    for dependency, dependant in pairs:
        if dependant not in dependencies:
            dependencies[dependant] = []
        if dependency not in dependencies:
            dependencies[dependency] = []
        dependencies[dependant].append(dependency)
    return dependencies


def part1(dependencies: Dict[str, List[str]]) -> str:
    path: List[str] = []
    while dependencies:
        next_step: str = next(
            step for step, step_dependencies in dependencies.items() if not step_dependencies)
        del dependencies[next_step]
        path.append(next_step)
        for step_dependencies in dependencies.values():
            if next_step in step_dependencies:
                step_dependencies.remove(next_step)
    return "".join(path)


def part2(dependencies: Dict[str, List[str]]) -> int:
    WORKER_COUNT = 5
    STEP_DURATION_OFFSET = ord("A") - 60 - 1
    running_workers: Dict[str, int] = {}
    seconds = 0
    while dependencies or running_workers:
        to_remove: List[str] = []
        for step in running_workers.keys():
            running_workers[step] -= 1
            if running_workers[step] == 0:
                to_remove.append(step)
        for step in to_remove:
            del running_workers[step]
            for step_dependencies in dependencies.values():
                if step in step_dependencies:
                    step_dependencies.remove(step)
        next_steps = iter(sorted(
            step for step, step_dependencies in dependencies.items() if not step_dependencies))
        next_step = next(next_steps, None)
        while len(running_workers) <= WORKER_COUNT and next_step:
            running_workers[next_step] = ord(next_step) - STEP_DURATION_OFFSET
            del dependencies[next_step]
            next_step = next(next_steps, None)
        seconds += 1
    # because 1 seconds is counted after emptying runningWorkers the last time
    return seconds - 1


def solve(pairs: List[Tuple[str, str]]) -> Tuple[str, int]:
    dependencies = build_dependency_graph(pairs)
    return (
        part1({k: list(v) for k, v in dependencies.items()}),
        part2(dependencies)
    )


def get_input(file_path: str) -> List[Tuple[str, str]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    line_regex = re.compile(r"\s([A-Z])\s")
    with open(file_path, "r") as file:
        return [tuple(line_regex.findall(line.strip())) for line in file.readlines()]


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
