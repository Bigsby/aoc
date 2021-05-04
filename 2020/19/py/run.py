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
    def __init__(self, definition: str):
        match = letter_regex.match(definition)
        if match:
            self.type = RuleType.Letter
            self.letter = match.group("letter")
        else:
            self.type = RuleType.Set
            self.sets: List[List[int]] = []
            for set in definition.split("|"):
                self.sets.append(
                    list(map(lambda rule: int(rule), set.strip().split(" "))))


def find_matched_indexes(rules: Dict[int, Rule], string: str, rule_number: int = 0, index: int = 0) -> List[int]:
    if index == len(string):
        return []
    rule = rules[rule_number]
    if rule.type == RuleType.Letter:
        if string[index] == rule.letter:
            return [index + 1]
        return []
    matches: List[int] = []
    for rule_set in rule.sets:
        sub_matches = [index]
        for sub_rule in rule_set:
            new_matches: List[int] = []
            for sub_match_index in sub_matches:
                new_matches += find_matched_indexes(rules, string, sub_rule, sub_match_index)
            sub_matches = new_matches
        matches += sub_matches
    return matches


def solve(puzzle_input: Tuple[Dict[int, Rule], List[str]]) -> Tuple[int, int]:
    rules, messages = puzzle_input
    part1_result = sum(1 for message in messages if len(
        message) in find_matched_indexes(rules, message))
    rules[8] = Rule("42 | 42 8")
    rules[11] = Rule("42 31 | 42 11 31")
    return (
        part1_result,
        sum(1 for message in messages if len(message) in find_matched_indexes(rules, message))
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
                    rules[int(match.group("number"))] = Rule(match.group("rule"))
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
