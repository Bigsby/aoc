#! /usr/bin/python3

import sys, os, time
import re
from typing import Tuple, List

Input = List[Tuple[Tuple[str,int,int],List[str]]]


def p1(homework) -> int:
    total = 0
    for op, values in homework:
        operation, start, end = op
        sub_total = 0 if operation == '+' else 1
        for value in values:
            number = int(value.strip())
            if operation == '+':
                sub_total += number
            else:
                sub_total *= number
        total += sub_total
    return total


def p2(homework) -> int:
    total = 0
    for op, values in homework:
        operation, start, end = op
        sub_total = 0 if operation == '+' else 1
        for index in range(end - start):
            digits = [ str(number[index]) for number in values]
            if all([ d == ' ' for d in digits]):
                continue
            value = int("".join(digits).strip())
            if operation == '+':
                sub_total += value
            else:
                sub_total *= value
        total += sub_total
    return total


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (p1(puzzle_input), p2(puzzle_input))


operations_regex = re.compile(r"([\+|\*] +)")
def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        lines = file.readlines()
        operations_line = lines[-1]
        values = lines[:-1]
        homework = []
        for match in operations_regex.finditer(operations_line):
            operation, start, end = match.group(1).strip(), match.start(1), match.end(1)
            homework.append(((operation, start, end), [ line[start:end] for line in values ]))

        return homework


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
