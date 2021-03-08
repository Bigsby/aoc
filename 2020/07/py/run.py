#! /usr/bin/python3

import sys
import os
import time
import re
from typing import Dict, Iterable, List, Tuple

Rule = Tuple[str, int]
Rules = Dict[str, List[Rule]]
REQUIRED_COLOR = "shiny gold"


def get_rules_containing(color: str, rules: Rules) -> Iterable[str]:
    for rule_color, inner_rules in rules.items():
        if any(map(lambda inner_rule: inner_rule[0] == color, inner_rules)):
            yield rule_color
            yield from get_rules_containing(rule_color, rules)


def get_quantity_from_color(color: str, rules: Rules) -> int:
    return sum(map(lambda inner_rule: inner_rule[1] * (1 + get_quantity_from_color(inner_rule[0], rules)), rules[color]))


def solve(rules: Rules) -> Tuple[int, int]:
    return (
        len(set(get_rules_containing(REQUIRED_COLOR, rules))),
        get_quantity_from_color(REQUIRED_COLOR, rules)
    )


inner_bags_regex = re.compile(r"^(\d+)\s(.*)\sbags?$")
bags_regex = re.compile(r"^(.*)\sbags contain\s(.*)$")


def process_inner_rule(text: str) -> Rule:
    match = inner_bags_regex.match(text.strip())
    if match:
        return (match.group(2), int(match.group(1)))
    raise Exception("Bad format", text)


def process_inner_rules(text: str) -> List[Rule]:
    if text == "no other bags":
        return []
    return [process_inner_rule(innerText) for innerText in text.split(", ")]


def process_line(line: str) -> Tuple[str, List[Rule]]:
    match = bags_regex.match(line)
    if match:
        return (match.group(1), process_inner_rules(match.group(2).rstrip(".")))
    raise Exception("Bad format", line)


def get_input(file_path: str) -> Rules:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return {color: innerRules for color, innerRules in [process_line(line) for line in file.readlines()]}


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1_result, part_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
