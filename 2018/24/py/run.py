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
        self.hitPoints = hit
        self.immunities = immunities
        self.weaknesses = weaknesses
        self.initiative = inititive
        self.type = type
        self.damage = damage
        self.army = army
        self.target: Optional['Group'] = None

    def effectivePower(self):
        return self.units * self.damage

    def damageTo(self, target: 'Group'):
        if self.type in target.immunities:
            return 0
        return self.effectivePower() * (2 if self.type in target.weaknesses else 1)

    def Clone(self, boost: int) -> 'Group':
        return Group(self.id, self.units, self.hitPoints, self.immunities, self.weaknesses, self.initiative, self.type, self.damage + boost, self.army)


def combat(groups: List[Group], boost: int) -> Tuple[int, int]:
    groups = [group.Clone(boost if group.army == 0 else 0) for group in groups]
    while True:
        groups = sorted(
            groups, key=lambda u: (-u.effectivePower(), -u.initiative))
        selectedTargets: Set[str] = set()
        for group in groups:
            targets = [target for target in groups
                       if target.army != group.army and target.id not in selectedTargets and group.damageTo(target) > 0]
            if targets:
                targets.sort(key=lambda target: (-group.damageTo(target), -
                                                 target.effectivePower(), -target.initiative))
                group.target = targets[0]
                selectedTargets.add(group.target.id)
        groups = sorted(groups, key=lambda group: -group.initiative)
        unitsKilled = False
        for group in groups:
            if group.target:
                killed = min(group.target.units, group.damageTo(
                    group.target) // group.target.hitPoints)
                unitsKilled |= killed > 0
                group.target.units -= killed
        groups = [group for group in groups if group.units > 0]
        for group in groups:
            group.target = None
        immuneSystemUnits = sum(
            [group.units for group in groups if group.army == 0])
        infectionUnits = sum(
            [group.units for group in groups if group.army == 1])
        if not unitsKilled or immuneSystemUnits == 0:
            return 1, infectionUnits
        if infectionUnits == 0:
            return 0, immuneSystemUnits


def solve(groups: List[Group]) -> Tuple[int, int]:
    boost = 0
    while True:
        boost += 1
        winner, left = combat(groups, boost)
        if winner == 0:
            return combat(groups, 0)[1], left


numbersRegex = re.compile(
    r"^(?P<units>\d+) units.*with (?P<hit>\d+) hit.*does (?P<damage>\d+) (?P<type>\w+).*initiative (?P<initiative>\d+)$")
immunityWeaknessRegex = re.compile(r"\(.*\)")


def parseGroup(text: str, army: int, number: int) -> Group:
    numberMatch = numbersRegex.match(text)
    if numberMatch:
        immunities: List[str] = []
        weaknesses: List[str] = []
        immunityWeaknessMatch = immunityWeaknessRegex.search(text)
        if immunityWeaknessMatch:
            for group in immunityWeaknessMatch.group()[1:-1].split(";"):
                if group.strip().startswith("weak"):
                    weaknesses = list(
                        map(str.strip, group.strip()[8:].split(",")))
                elif group.strip().startswith("immune"):
                    immunities = list(
                        map(str.strip, group.strip()[10:].split(",")))
        return Group(
            f"{army}{number}",
            int(numberMatch.group("units")),
            int(numberMatch.group("hit")),
            immunities, weaknesses,
            int(numberMatch.group("initiative")),
            numberMatch.group("type"),
            int(numberMatch.group("damage")),
            army
        )
    raise Exception("Bad format", text)


def parseArmy(text: str, army: int) -> List[Group]:
    split = text.split("\n")
    groups: List[Group] = []
    for index, groupText in enumerate(split[1:]):
        groups.append(parseGroup(groupText, army, index + 1))
    return groups


def getInput(filePath: str) -> List[Group]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        armyTexts = file.read().split("\n\n")
        immuneSystem = parseArmy(armyTexts[0], 0)
        infection = parseArmy(armyTexts[1], 1)
        return [*immuneSystem, *infection]


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
