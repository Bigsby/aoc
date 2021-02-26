#! /usr/bin/python3

import sys, os, time
from typing import Iterable, Tuple
import re
from itertools import combinations

Player = Tuple[int,int,int]
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
    (102, 0,5)
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


def playGame(player: Player, boss: Player) -> bool:
    playerHit, playerDamage, playerArmor = player
    bossHit, bossDamage, bossArmor = boss
    playerDamage = max(1, playerDamage - bossArmor)
    bossDamage = max(1, bossDamage - playerArmor)
    while True:
        bossHit -= playerDamage
        if bossHit <= 0:
            return True
        playerHit -= bossDamage
        if playerHit <= 0:
            return False


def getInventoryCombinations() -> Iterable[Tuple[int,int,int]]:
    for weapon in WEAPONS:
        for armor in ARMORS:
            for ring1, ring2 in combinations(RINGS, 2):
                inventory = [ weapon, armor, ring1, ring2 ]
                cost, damage, defense = (sum(tool[index] for tool in inventory) for index in range(3))
                yield cost, damage, defense


def solve(boss: Player) -> Tuple[int,int]:
    minCost = sys.maxsize
    maxCost = 0
    for cost, damage, defense in getInventoryCombinations():
        if playGame((100, damage, defense), boss):
            minCost = min(minCost, cost)
        else:
            maxCost = max(maxCost, cost)
    return (minCost, maxCost)


inputRegex = re.compile(r"^Hit Points: (?P<hit>\d+)\W+Damage: (?P<damage>\d+)\W+^Armor: (?P<armor>\d+)", flags=re.MULTILINE)
def getInput(filePath: str) -> Player:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        match = inputRegex.match(file.read())
        if match:
            return int(match.group("hit")), int(match.group("damage")), int(match.group("armor"))
        else:
            raise Exception("Bad format input")


def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    start = time.perf_counter()
    part1Result, part2Result = solve(getInput(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()