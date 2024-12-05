#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Input = List[List[int]]


def is_report_safe(report: List[int]) -> bool:
    increasing = report[0] < report[-1]
    minimum_interval = -3 if increasing else 1
    maximum_interval = -1 if increasing else 3
    for index in range(len(report) - 1):
        difference = report[index] - report[index + 1]
        if difference == 0 or difference < minimum_interval or difference > maximum_interval:
            return False
    return True


def is_report_safe_skip(report: List[int], use_skip: bool) -> bool:
    is_safe = is_report_safe(report)
    if not is_safe and use_skip:
        for index_to_remove in range(len(report)):
            test_report = list(report)
            del test_report[index_to_remove]
            if is_report_safe(test_report):
                return True
    return is_safe


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (len([1 for report in puzzle_input if is_report_safe_skip(report, False)]), len([1 for report in puzzle_input if  is_report_safe_skip(report, True)]))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ [ int(level) for level in line.split() ] for line in file.readlines() ] 


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
