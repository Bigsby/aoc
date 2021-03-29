#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple
import re
from functools import reduce

Ticket = List[int]
Rule = Tuple[str, int, int, int, int]


def get_valid_numbers(rules: List[Rule]) -> Set[int]:
    valid_numbers: Set[int] = set()
    for _, start_one, end_one, start_two, end_two in rules:
        for number in range(start_one, end_one + 1):
            valid_numbers.add(number)
        for number in range(start_two, end_two + 1):
            valid_numbers.add(number)
    return valid_numbers


def part1(tickets: List[Ticket], valid_numbers: Set[int]) -> int:
    total = 0
    for ticket in tickets:
        for number in ticket:
            if number not in valid_numbers:
                total += number
    return total


def part2(rules: List[Rule], my_ticket: Ticket, tickets: List[Ticket], valid_numbers: Set[int]) -> int:
    valid_tickets: List[Ticket] = []
    for ticket in tickets:
        if all(number in valid_numbers for number in ticket):
            valid_tickets.append(ticket)
    ranges: Dict[str, Tuple[int, int, int, int]] = dict()
    positions: Dict[str, Set[int]] = dict()
    names: List[str] = []
    for name, *fieldRanges in rules:
        ranges[name] = tuple(fieldRanges)
        positions[name] = {i for i in range(0, len(rules))}
        names.append(name)
    for ticket in valid_tickets:
        for index, number in enumerate(ticket):
            for field_name in names:
                if index not in positions[field_name]:
                    continue
                start_one, end_one, start_two, end_two = ranges[field_name]
                if number < start_one or (number > end_one and number < start_two) or number > end_two:
                    to_remove: List[Tuple[str, int]] = []
                    positions[field_name].remove(index)
                    if len(positions[field_name]) == 1:
                        to_remove.append(
                            (field_name, next(iter((positions[field_name])))))
                    while len(to_remove):
                        owner_name, position_to_remove = to_remove.pop()
                        for other_field_name in names:
                            if other_field_name == owner_name or position_to_remove not in positions[other_field_name]:
                                continue
                            positions[other_field_name].remove(
                                position_to_remove)
                            if len(positions[other_field_name]) == 1:
                                to_remove.append((other_field_name, next(
                                    iter(positions[other_field_name]))))
    departure_field_indexes = [next(iter(positions[field_name]))
                               for field_name in names if field_name.startswith("departure")]
    result = reduce(lambda soFar, index: soFar *
                    my_ticket[index], departure_field_indexes, 1)
    return result


def solve(puzzle_input: Tuple[List[Rule], Ticket, List[Ticket]]) -> Tuple[int, int]:
    rules, my_ticket, tickets = puzzle_input
    valid_numbers = get_valid_numbers(rules)
    return (
        part1(tickets, valid_numbers),
        part2(rules, my_ticket, tickets, valid_numbers)
    )


field_regex = re.compile(
    r"^(?P<field>[^:]+):\s(?P<r1s>\d+)-(?P<r1e>\d+)\sor\s(?P<r2s>\d+)-(?P<r2e>\d+)$")
ticket_regex = re.compile(r"^(?:\d+\,)+(?:\d+$)")


def get_input(file_path: str) -> Tuple[List[Rule], Ticket, List[Ticket]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        rules: List[Rule] = []
        my_ticket: Ticket = list()
        tickets: List[Ticket] = []
        doing_rules = True
        doing_my_ticket = True
        for line in file.readlines():
            if doing_rules:
                field_match = field_regex.match(line)
                if field_match:
                    rules.append((field_match.group("field"), int(field_match.group("r1s")), int(
                        field_match.group("r1e")), int(field_match.group("r2s")), int(field_match.group("r2e"))))
                else:
                    doing_rules = False
            ticket_match = ticket_regex.match(line)
            if not ticket_match:
                continue
            if doing_my_ticket:
                my_ticket = list(map(int, line.split(",")))
                doing_my_ticket = False
            else:
                tickets.append(list(map(int, line.split(","))))
        return rules, my_ticket, tickets


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
