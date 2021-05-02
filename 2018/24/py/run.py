#! /usr/bin/python3

import sys
import os
import time
from typing import List, Optional, Set, Tuple
import re


class Group:
    def __init__(self, id: str, units: int, hit: int,
                 immunities: List[str], weaknesses: List[str],
                 inititive: int, type: str, damage: int, army: int):
        self.id = id
        self.units = units
        self.hit_points = hit
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.initiative = inititive
        self.type = type
        self.damage = damage
        self.army = army
        self.target: Optional['Group'] = None

    def effective_power(self):
        return self.units * self.damage

    def damage_to(self, target: 'Group'):
        if self.type in target.immunities:
            return 0
        return self.effective_power() * (2 if self.type in target.weaknesses else 1)

    def clone(self, boost: int) -> 'Group':
        return Group(self.id, self.units, self.hit_points, self.immunities, self.weaknesses, self.initiative, self.type, self.damage + boost, self.army)

    def __str__(self) -> str:
        return f"{self.id} {self.units} {self.hit_points} {self.damage} {self.effective_power()} {self.type} ({self.immunities}) ({self.weaknesses})"


def combat(groups: List[Group], boost: int) -> Tuple[int, int]:
    groups = [group.clone(boost if group.army == 0 else 0) for group in groups]
    while True:
        groups = sorted(
            groups, key=lambda u: (-u.effective_power(), -u.initiative))
        selected_targets: Set[str] = set()
        for group in groups:
            targets = [target for target in groups
                       if target.army != group.army and target.id not in selected_targets and group.damage_to(target) > 0]
            if targets:
                targets.sort(key=lambda target: (-group.damage_to(target), -
                                                 target.effective_power(), -target.initiative))
                group.target = targets[0]
                selected_targets.add(group.target.id)
        groups = sorted(groups, key=lambda group: -group.initiative)
        units_killed = False
        for group in groups:
            if group.target:
                killed = min(group.target.units, group.damage_to(
                    group.target) // group.target.hit_points)
                units_killed |= killed > 0
                group.target.units -= killed
        groups = [group for group in groups if group.units > 0]
        for group in groups:
            group.target = None
        immune_system_units = sum(
            [group.units for group in groups if group.army == 0])
        infection_units = sum(
            [group.units for group in groups if group.army == 1])
        if not units_killed or immune_system_units == 0:
            return 1, infection_units
        if infection_units == 0:
            return 0, immune_system_units


def solve(groups: List[Group]) -> Tuple[int, int]:
    boost = 0
    while True:
        boost += 1
        winner, left = combat(groups, boost)
        if winner == 0:
            return combat(groups, 0)[1], left


numbers_regex = re.compile(
    r"^(?P<units>\d+) units.*with (?P<hit>\d+) hit.*does (?P<damage>\d+) (?P<type>\w+).*initiative (?P<initiative>\d+)$")
immunity_weakness_regex = re.compile(r"\(.*\)")


def parse_group(text: str, army: int, number: int) -> Group:
    number_match = numbers_regex.match(text)
    if number_match:
        immunities: List[str] = []
        weaknesses: List[str] = []
        immunity_weakness_match = immunity_weakness_regex.search(text)
        if immunity_weakness_match:
            for group in immunity_weakness_match.group()[1:-1].split(";"):
                if group.strip().startswith("weak"):
                    weaknesses = list(
                        map(str.strip, group.strip()[8:].split(",")))
                elif group.strip().startswith("immune"):
                    immunities = list(
                        map(str.strip, group.strip()[10:].split(",")))
        return Group(
            f"{army}{number}",
            int(number_match.group("units")),
            int(number_match.group("hit")),
            immunities, weaknesses,
            int(number_match.group("initiative")),
            number_match.group("type"),
            int(number_match.group("damage")),
            army
        )
    raise Exception("Bad format", text)


def parse_army(text: str, army: int) -> List[Group]:
    split = text.split("\n")
    groups: List[Group] = []
    for index, group_text in enumerate(split[1:]):
        if group_text:
            groups.append(parse_group(group_text, army, index + 1))
    return groups


def get_input(file_path: str) -> List[Group]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        army_texts = file.read().split("\n\n")
        immune_system = parse_army(army_texts[0], 0)
        infection = parse_army(army_texts[1], 1)
        return [*immune_system, *infection]


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
