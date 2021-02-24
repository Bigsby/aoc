#! /usr/bin/python3

import sys, os, time
from typing import Dict, List, Tuple

Position = complex
Walls = List[Position]
Team = Dict[Position,int]


def drawGame(walls: Walls, elves: Team, goblins: Team):
    maxX = int(max(map(lambda w: w.real, walls)))
    minY = int(min(map(lambda w: w.imag, walls)))
    for y in range(0, minY - 1, -1):
        for x in range(0, maxX + 1):
            position = x + y * 1j
            c = "."
            if position in walls:
                c = "#"
            elif position in elves:
                c = "E"
            elif position in goblins:
                c = "G"
            print(c, end="")
        print()
    print(elves)
    print(goblins)
    print()


ATTACK_DIRECTIONS = [ 1j, -1, 1, -1j ]


def getAttackPositions(mates: Team, enemies: Team, walls: Walls) -> List[complex]:
    attackPositions = set()
    for enemy in enemies.keys():
        for direction in ATTACK_DIRECTIONS:
            attackPosition = enemy + direction
            if attackPosition not in mates and attackPosition not in enemies and attackPosition not in walls:
                attackPositions.add(attackPosition)
    return list(sorted(attackPositions, key=lambda p: (p.imag, p.real)))


def attack(unitPosition: complex, enemies: Team, attackPower: int) -> bool:
    targets = []
    for direction in ATTACK_DIRECTIONS:
        enemyPosition = unitPosition + direction
        if enemyPosition in enemies:
            targets.append((enemies[enemyPosition], enemyPosition))
    if targets:
        targets.sort(key=lambda t: (t[0], -t[1].imag, t[1].real))
        targetPosition = targets[0][1]
        enemies[targetPosition] -= attackPower
        if enemies[targetPosition] <= 0:
            del enemies[targetPosition]
        return True
    return False


MOVE_DIRECTIONS = [ -1j, 1j, -1, 1 ]
def getMove(start: Position, targets: List[Position], invalidPositions: Walls) -> Position:
    firstMoves = [ start + direction for direction in MOVE_DIRECTIONS ]
    firstMoves = [ x for x in firstMoves if  x not in invalidPositions ]
    bestMoves = []
    for move in firstMoves:
        if move in targets:
            bestMoves.append((move, 1, move))
            continue
        seenPositions = { start, move }
        stack = [ move + direction for direction in MOVE_DIRECTIONS ]
        stack = [ m for m in stack if m not in invalidPositions ]
        length = 1
        run = True
        while run:
            length += 1
            newStack: List[Position] = []
            for newPosition in stack:
                if newPosition in seenPositions:
                    continue
                seenPositions.add(newPosition)
                if newPosition in targets:
                    bestMoves.append((move, length, newPosition))
                    run = False
                    continue
                newTiles = [ newPosition + direction for direction in MOVE_DIRECTIONS ]
                newStack += [ newTile for newTile in newTiles if newTile not in seenPositions and newTile not in invalidPositions ]
            stack = list(newStack)
            if not stack:
                run = False
    if not bestMoves:
        return -1
    minLength = min([x[1] for x in bestMoves])
    bestMoves = [x for x in bestMoves if x[1]==minLength]
    bestMoves.sort(key = lambda x: (-x[2].imag, x[2].real, -x[0].imag, x[0].real))
    return bestMoves[0][0]


def makeUnitTurn(unitPosition: complex, mates: Team, enemies: Team, walls: Walls, attackPower: int) -> Position:
    if attack(unitPosition, enemies, attackPower):
        return unitPosition
    attackPositions = getAttackPositions(mates, enemies, walls)
    wholeMap = [ *mates.keys(), *enemies.keys(), *walls ]
    newPosition = getMove(unitPosition, attackPositions, wholeMap)
    if newPosition != -1:
        hitPoints = mates[unitPosition]
        del mates[unitPosition]
        mates[newPosition] = hitPoints
        attack(newPosition, enemies, attackPower)
        return newPosition
    return unitPosition


DEFAULT_POWER = 3


def makeRound(walls: Walls, elves: Team, goblins: Team, elfPower: int):
    unitsToPlay = sorted([ * elves, *goblins ], key=lambda p: (-p.imag, p.real))
    newPositions = []
    while unitsToPlay:
        position = unitsToPlay.pop(0)
        if position in newPositions:
            continue
        newPosition = -1
        if position in goblins:
            if not elves:
                return False
            newPosition = makeUnitTurn(position, goblins, elves, walls, DEFAULT_POWER)
            newPositions.append(newPosition)
        elif position in elves:
            if not goblins:
                return False
            newPosition = makeUnitTurn(position, elves, goblins, walls, elfPower)
        newPositions.append(newPosition)
    return True


def runGame(walls: Walls, elves: Team, goblins: Team, allElves: bool, elfPower: int = DEFAULT_POWER) -> Tuple[bool,int]:
    elves = dict(elves)
    startingElves = len(elves)
    goblins = dict(goblins)
    round = 0
    while makeRound(walls, elves, goblins, elfPower) and not (allElves and len(elves) != startingElves):
        round += 1
    return len(elves) == startingElves, round * (sum(elves.values()) + sum(goblins.values()))


def part1(game: Tuple[Walls,Team,Team]) -> int:
    walls, elves, goblins = game
    _, result = runGame(walls, elves, goblins, False)
    return result


def part2(game: Tuple[Walls,Team,Team]) -> int:
    walls, elves, goblins = game
    elfPower = 10
    while True:
        elfPower += 1
        success, result = runGame(walls, elves, goblins, True, elfPower)
        if success:
            return result


WALL = "#"
ELF = "E"
GOBLIN = "G"
STARTING_HITPOINTS = 200
def getInput(filePath: str) -> Tuple[Walls,Team,Team]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)

    with open(filePath, "r") as file:
        walls = []
        elves = {}
        goblins = {}
        for y, line in enumerate(file.readlines()):
            for x, c in enumerate(line.strip()):
                position = x - y * 1j
                if c == WALL:
                    walls.append(position)
                elif c == ELF:
                    elves[position] = STARTING_HITPOINTS
                elif c == GOBLIN:
                    goblins[position] = STARTING_HITPOINTS
        return walls, elves, goblins



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
    print(f"P1 time: {middle - start:.7f}")
    print(f"P2 time: {end - middle:.7f}")


if __name__ == "__main__":
    main()