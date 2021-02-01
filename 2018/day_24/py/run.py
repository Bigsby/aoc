#! /usr/bin/python3

import sys, os, time
from typing import List
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
        self.target = None

    def effectivePower(self):
        return self.units * self.damage

    def damageTo(self, target: 'Group'):
        if self.type in target.immunities:
            return 0
        return self.effectivePower() * (2 if self.type in target.weaknesses else 1)


def combat(original_units: List[Group], boost: int):
    groups = []
    for group in original_units:
        new_dmg = group.damage + (boost if group.army==0 else 0)
        groups.append(Group(group.id, group.units, group.hitPoints, group.immunities, 
                group.weaknesses, group.initiative, group.type, new_dmg, group.army))

    while True:
        groups = sorted(groups, key=lambda u: (-u.effectivePower(), -u.initiative))
        selectedTargets = set()
        for group in groups:
            targets = [target for target in groups 
                if target.army != group.army and target.id not in selectedTargets and group.damageTo(target) > 0 ]
            if targets:
                targets.sort(key=lambda target: (-group.damageTo(target), -target.effectivePower(), -target.initiative))
                group.target = targets[0]
                selectedTargets.add(group.target.id)
        groups = sorted(groups, key=lambda group: -group.initiative)
        unitsKilled = False
        for group in groups:
            if group.target:
                dmg = group.damageTo(group.target)
                killed = min(group.target.units, dmg // group.target.hitPoints)
                if killed > 0:
                    unitsKilled = True
                group.target.units -= killed

        groups = [group for group in groups if group.units > 0]
        for group in groups:
            group.target = None

        immuneSystemUnits = sum([group.units for group in groups if group.army == 0])
        infectionUnits = sum([group.units for group in groups if group.army == 1])
        if not unitsKilled:
            return 1,infectionUnits
        if immuneSystemUnits == 0:
            return 1,infectionUnits
        if infectionUnits == 0:
            return 0,immuneSystemUnits
        


def part1(groups: List[Group]) -> int:
    _, left = combat(groups, 0)
    return left


def part2(groups: List[Group]) -> int:
    boost = 0
    left = 0
    while True:
        boost += 1
        winner, left = combat(groups, boost)
        if winner == 0:
            break
    return left
    


numbersRegex = re.compile(r"^(?P<units>\d+) units.*with (?P<hit>\d+) hit.*does (?P<damage>\d+) (?P<type>\w+).*initiative (?P<initiative>\d+)$")
immunityWeaknessRegex = re.compile(r"\(.*\)")
def parseGroup(text:str, army: int, number: int) -> Group:
    numberMatch = numbersRegex.match(text)
    if numberMatch:
        immunities = []
        weaknesses = []
        immunityWeaknessMatch = immunityWeaknessRegex.search(text)
        if immunityWeaknessMatch:
            for group in immunityWeaknessMatch.group()[1:-1].split(";"):
                if group.strip().startswith("weak"):
                    weaknesses = list(map(str.strip, group.strip()[8:].split(",")))
                elif group.strip().startswith("immune"):
                    immunities = list(map(str.strip, group.strip()[10:].split(",")))
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
    groups = []
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
        return [ *immuneSystem, *infection ]



def main():
    if len(sys.argv) != 2:
        raise Exception("Please, add input file path as parameter")

    puzzleInput = getInput(sys.argv[1])
    start = time.perf_counter()
    part1Result = part1(puzzleInput)
    middle = time.perf_counter()
    part2Result = part2(puzzleInput)
    end = time.perf_counter()
    print("P1:", part1Result)
    print("P2:", part2Result)
    print()
    print(f"P1 time: {middle - start:.8f}")
    print(f"P2 time: {end - middle:.8f}")


if __name__ == "__main__":
    main()