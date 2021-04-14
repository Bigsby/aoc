#! /usr/bin/python3

import sys
import os
import time
from typing import List, Tuple
import re

Spell = Tuple[int, int, int, int, int, int]

SPELLS = [  # cost, damage, hitPoints, armor, mana, duration
    (53,  4, 0, 0,   0, 0),  # Magic Missile
    (73,  2, 2, 0,   0, 0),  # Drain
    (113, 0, 0, 7,   0, 6),  # Shield
    (173, 3, 0, 0,   0, 6),  # Poison
    (229, 0, 0, 0, 101, 5)  # Recharge
]


def get_least_winning_mana(data: Tuple[int, ...], lose_hit_on_player_turn: bool) -> int:
    boss_hit, boss_damage = data
    least_mana_spent = sys.maxsize
    queue: List[Tuple[int, int, int, List[Spell], bool, int]] = [
        (boss_hit, 50, 500, [], True, 0)]
    while queue:
        boss_hit, player_hit, player_mana, active_spells, player_turn, mana_spent = queue.pop()
        if lose_hit_on_player_turn and player_turn:
            player_hit -= 1
            if player_hit <= 0:
                continue
        player_armor = 0
        new_active_spells: List[Spell] = []
        for active_spell in active_spells:
            cost, damage, hit_points, armor, mana, duration = active_spell
            if duration >= 0:
                boss_hit -= damage
                player_hit += hit_points
                player_armor += armor
                player_mana += mana
            if duration > 1:
                new_active_spells.append(
                    (cost, damage, hit_points, armor, mana, duration - 1))
        if boss_hit <= 0:
            least_mana_spent = min(least_mana_spent, mana_spent)
            continue
        if mana_spent > least_mana_spent:
            continue
        if player_turn:
            active_costs = [spell[0] for spell in new_active_spells]
            for spell in SPELLS:
                spell_cost = spell[0]
                # cost is unique per spell
                if spell_cost not in active_costs and spell_cost <= player_mana:
                    queue.append((boss_hit, player_hit, player_mana - spell_cost,
                                  new_active_spells + [spell], False, mana_spent + spell_cost))
        else:
            player_hit -= max(1, boss_damage - player_armor)
            if player_hit > 0:
                queue.append((boss_hit, player_hit, player_mana,
                              new_active_spells, True, mana_spent))
    return least_mana_spent


def solve(data: Tuple[int, int]) -> Tuple[int, int]:
    return (
        get_least_winning_mana(data, False),
        get_least_winning_mana(data, True)
    )


def get_input(file_path: str) -> Tuple[int, ...]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        return tuple(map(int, re.findall(r"(\d+)", file.read())))


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
