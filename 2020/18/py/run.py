#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re


def get_next_token(expression: str) -> Tuple[str, str]:
    current_token = ""
    for index, c in enumerate(expression):
        if c == " ":
            return current_token, expression[index + 1:].strip()
        if current_token.isdigit() and not c.isdigit():
            return current_token, expression[index:].strip()
        current_token += c
    return current_token, ""


def perform_operation(first: int, operation: str, second: int) -> int:
    if operation == "*":
        return first * second
    if operation == "+":
        return first + second
    raise Exception(f"Unknow operation {operation}")


paren_regex = re.compile(r"\((?P<expression>[^()]+)\)")
plus_regex = re.compile(r"(?P<first>\d+)\s\+\s(?P<second>\d+)")


def evaluate_expression(expression: str, add_first: bool) -> int:
    paren_match = paren_regex.search(expression)
    while paren_match:
        expression = "".join([expression[:paren_match.start()], str(evaluate_expression(
            paren_match.group("expression"), add_first)), expression[paren_match.end():]])
        paren_match = paren_regex.search(expression)

    if add_first:
        plus_match = plus_regex.search(expression)
        while plus_match:
            expression = "".join([expression[:plus_match.start()], str(int(plus_match.group(
                "first")) + int(plus_match.group("second"))), expression[plus_match.end():]])
            plus_match = plus_regex.search(expression)

    token, expression = get_next_token(expression)
    current_value = int(token)
    operation_to_perform = ""
    while expression:
        token, expression = get_next_token(expression)
        if token.isdigit():
            current_value = perform_operation(
                current_value, operation_to_perform, int(token))
        else:
            operation_to_perform = token
    return current_value


def evaluate_expressions(add_first: bool, expressions: List[str]) -> int:
    return sum([evaluate_expression(expression, add_first) for expression in expressions])


def solve(expressions: List[str]) -> Tuple[int, int]:
    return (
        evaluate_expressions(False, expressions),
        evaluate_expressions(True, expressions)
    )


def get_input(file_path: str) -> List[str]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return file.readlines()


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
