#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple
import re


SPELLS = [ # cost, damage, hitPoints, armor, mana, duration
    (53,  4, 0, 0,   0, 0), # Magic Missile
    (73,  2, 2, 0,   0, 0), # Drain
    (113, 0, 0, 7,   0, 6), # Shield
    (173, 3, 0, 0,   0, 6), # Poison
    (229, 0, 0, 0, 101, 5)  # Recharge
]
def getLeastWinningMana(bossHit: int, bossDamage: int, loseHitOnPlayerTurn: bool) -> int:
    leastManaSpent = sys.maxsize
    queue: List[Tuple[int,int,int,List[Tuple[int,...]],bool,int]] = [(bossHit, 50, 500, [], True, 0)]
    while queue:
        bossHit, playerHit, playerMana, activeSpells, playerTurn, manaSpent = queue.pop()
        if loseHitOnPlayerTurn and playerTurn:
            playerHit -= 1
            if playerHit <= 0:
                continue

        playerArmor = 0
        newActiveSpells = []
        for activeSpell in activeSpells:
            cost, damage, hitPoints, armor, mana, duration = activeSpell
            if duration >= 0:
                bossHit -= damage
                playerHit += hitPoints
                playerArmor += armor
                playerMana += mana
            if duration > 1:
                newActiveSpells.append((cost, damage, hitPoints, armor, mana, duration - 1))

        if bossHit <= 0:
            if manaSpent < leastManaSpent:
                leastManaSpent = manaSpent
            continue
        if manaSpent > leastManaSpent:
            continue

        if playerTurn:
            activeCosts = [ spell[0] for spell in newActiveSpells ] # cost is unique per spell
            for spell in SPELLS:
                spellCost = spell[0]
                if spellCost not in activeCosts and spellCost <= playerMana:
                    queue.append((bossHit, playerHit, playerMana - spellCost, newActiveSpells + [spell], False, manaSpent + spellCost))
        else:
            playerHit -= max(1, bossDamage - playerArmor)
            if playerHit > 0:
                queue.append((bossHit, playerHit, playerMana, newActiveSpells, True, manaSpent))

    return leastManaSpent


def part1(data: Tuple[int,int]) -> int:
    bossHit, bossDamage = data
    return getLeastWinningMana(bossHit, bossDamage, False)

        
def part2(data: Tuple[int,int]) -> int:
    bossHit, bossDamage = data
    return getLeastWinningMana(bossHit, bossDamage, True)


def getInput(filePath: str) -> Tuple[int,int]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        return tuple(map(int, re.findall(r"(\d+)", file.read())))


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