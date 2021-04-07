#! /usr/bin/python3

import sys
import os
import time
import re
from enum import Enum
from typing import Dict, List, Tuple


class RuleType(Enum):
    Letter = 0
    Set = 1


letter_regex = re.compile(r"^\"(?P<letter>a|b)\"$")


class Rule():
    def __init__(self, number: str, definition: str):
        match = letter_regex.match(definition)
        self.number = int(number)
        if match:
            self.type = RuleType.Letter
            self.letter = match.group("letter")
        else:
            self.type = RuleType.Set
            self.sets: List[List[int]] = []
            for set in definition.split("|"):
                self.sets.append(
                    list(map(lambda rule: int(rule), set.strip().split(" "))))


def generate_regex(rules: Dict[int, Rule], rule_number: int) -> str:
    rule = rules[rule_number]
    if rule.type == RuleType.Letter:
        return rule.letter
    else:
        return "(?:" + \
            "|".join("".join(generate_regex(rules, inner_number)
                             for inner_number in rule_set) for rule_set in rule.sets) + ")"


def is_inner_match(rule: str, message: str, position: int) -> Tuple[bool, int]:
    match = re.match(rule, message[position:])
    if match:
        return True, position + match.end()
    return False, position


def is_match(first_rule: str, second_rule: str, message: str) -> bool:
    count = 0
    matched, position = is_inner_match(first_rule, message, 0)
    while matched and position < len(message):
        last_position = position
        for _ in range(count):
            matched, position = is_inner_match(second_rule, message, position)
            if not matched:
                position = last_position
                break
            elif position == len(message):
                return True
        count += 1
        matched, position = is_inner_match(first_rule, message, position)
    return False


def solve(puzzle_input: Tuple[Dict[int, Rule], List[str]]) -> Tuple[int, int]:
    rules, messages = puzzle_input
    rule_0 = generate_regex(rules, 0)
    rule_42 = "^" + generate_regex(rules, 42)
    rule_31 = "^" + generate_regex(rules, 31)
    return (
        sum(1 for message in messages if re.fullmatch(rule_0, message)),
        sum(1 for message in messages if is_match(rule_42, rule_31, message))
    )


rule_regex = re.compile(r"(?P<number>^\d+):\s(?P<rule>.+)$")


def get_input(file_path: str) -> Tuple[Dict[int, Rule], List[str]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        rules: Dict[int, Rule] = {}
        messages: List[str] = []
        for line in file.readlines():
            if line.strip() != "":
                match = rule_regex.match(line)
                if match:
                    rules[int(match.group("number"))] = Rule(
                        match.group("number"), match.group("rule"))
                else:
                    messages.append(line.strip())
        return rules, messages


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
