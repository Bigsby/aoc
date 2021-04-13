#! /usr/bin/python3

import sys
import os
import time
from typing import Iterable, Tuple
import re
from itertools import combinations

Player = Tuple[int, int, int]
WEAPONS = [
    (8, 4, 0),
    (10, 5, 0),
    (25, 6, 0),
    (40, 7, 0),
    (74, 8, 0)
]
ARMORS = [
    (0, 0, 0),
    (13, 0, 1),
    (31, 0, 2),
    (53, 0, 3),
    (75, 0, 4),
    (102, 0, 5)
]
RINGS = [
    (0, 0, 0),
    (0, 0, 0),
    (25, 1, 0),
    (50, 2, 0),
    (100, 3, 0),
    (20, 0, 1),
    (40, 0, 2),
    (80, 0, 3)
]


def play_game(player: Player, boss: Player) -> bool:
    player_hit, player_damage, player_armor = player
    boss_hit, boss_damage, boss_armor = boss
    player_damage = max(1, player_damage - boss_armor)
    boss_damage = max(1, boss_damage - player_armor)
    while True:
        boss_hit -= player_damage
        if boss_hit <= 0:
            return True
        player_hit -= boss_damage
        if player_hit <= 0:
            return False


def get_inventory_combinations() -> Iterable[Tuple[int, int, int]]:
    for weapon in WEAPONS:
        for armor in ARMORS:
            for ring1, ring2 in combinations(RINGS, 2):
                inventory = [weapon, armor, ring1, ring2]
                cost, damage, defense = (
                    sum(tool[index] for tool in inventory) for index in range(3))
                yield cost, damage, defense


def solve(boss: Player) -> Tuple[int, int]:
    min_cost = sys.maxsize
    max_cost = 0
    for cost, damage, defense in get_inventory_combinations():
        if play_game((100, damage, defense), boss):
            min_cost = min(min_cost, cost)
        else:
            max_cost = max(max_cost, cost)
    return (min_cost, max_cost)


input_regex = re.compile(
    r"^Hit Points: (?P<hit>\d+)\W+Damage: (?P<damage>\d+)\W+^Armor: (?P<armor>\d+)", flags=re.MULTILINE)


def get_input(file_path: str) -> Player:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        match = input_regex.match(file.read())
        if match:
            return int(match.group("hit")), int(match.group("damage")), int(match.group("armor"))
        else:
            raise Exception("Bad format input")


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
