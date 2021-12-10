#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List
from queue import LifoQueue

matches = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
}

illegal_closing_points = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

closing_points = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def solve(lines: List[str]) -> Tuple[int,int]:
    incomplete_points = []
    illegal_points = 0
    for line in lines:
        expected_closing = LifoQueue()
        illegal = False
        for c in line:
            if c == '(' or c == '[' or c == '{' or c == '<':
                expected_closing.put(matches[c])
            elif c != expected_closing.get():
                illegal = True
                illegal_points += illegal_closing_points[c]
                break
        if not illegal:
            points = 0
            while not expected_closing.empty():
                points = points * 5 + closing_points[expected_closing.get()]
            incomplete_points.append(points)
    incomplete_points.sort()
    return illegal_points, incomplete_points[int(len(incomplete_points) / 2)]


    return (part1(lines), part2(lines))


def get_input(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        return [ line.strip() for line in file.readlines() ]


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
