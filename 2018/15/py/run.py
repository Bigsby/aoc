#! /usr/bin/python3

import sys
import os
import time
from typing import Dict, List, Set, Tuple

Position = complex
Walls = List[Position]
Team = Dict[Position, int]
WALL = "#"
ELF = "E"
GOBLIN = "G"
STARTING_HITPOINTS = 200


def draw_game(walls: Walls, elves: Team, goblins: Team):
    print(chr(27) + "[2J")
    max_x = int(max(map(lambda w: w.real, walls)))
    min_y = int(min(map(lambda w: w.imag, walls)))
    for y in range(0, min_y - 1, -1):
        for x in range(0, max_x + 1):
            position = x + y * 1j
            c = "."
            if position in walls:
                c = WALL
            elif position in elves:
                c = ELF
            elif position in goblins:
                c = GOBLIN
            print(c, end="")
        print()
    print(elves)
    print(goblins)
    print()
    input()


ATTACK_DIRECTIONS = [1j, -1, 1, -1j]


def get_attack_positions(mates: Team, enemies: Team, walls: Walls) -> List[Position]:
    attack_positions: Set[Position] = set()
    for enemy in enemies.keys():
        for direction in ATTACK_DIRECTIONS:
            attack_position = enemy + direction
            if attack_position not in mates and attack_position not in enemies and attack_position not in walls:
                attack_positions.add(attack_position)
    return list(attack_positions)


def attack(unit_position: Position, enemies: Team, attack_power: int) -> bool:
    targets: List[Tuple[int, Position]] = []
    for direction in ATTACK_DIRECTIONS:
        enemy_position = unit_position + direction
        if enemy_position in enemies:
            targets.append((enemies[enemy_position], enemy_position))
    if targets:
        targets.sort(key=lambda t: (t[0], -t[1].imag, t[1].real))
        target_position = targets[0][1]
        enemies[target_position] -= attack_power
        # print(unit_position, "attacks", target_position, enemies[target_position]); input()
        if enemies[target_position] <= 0:
            # print(target_position, "dies")
            # input()
            del enemies[target_position]
        return True
    return False


MOVE_DIRECTIONS = [-1j, 1j, -1, 1]


def get_move(start: Position, targets: List[Position], invalid_positions: Walls) -> Position:
    first_moves = [start + direction for direction in MOVE_DIRECTIONS]
    first_moves = [x for x in first_moves if x not in invalid_positions]
    best_moves: List[Tuple[Position, int, Position]] = []
    for move in first_moves:
        if move in targets:
            best_moves.append((move, 1, move))
            continue
        seen_positions = {start, move}
        stack = [move + direction for direction in MOVE_DIRECTIONS if move +
                 direction not in invalid_positions]
        length = 1
        run = True
        while run:
            length += 1
            new_stack: List[Position] = []
            for new_position in stack:
                if new_position in seen_positions:
                    continue
                seen_positions.add(new_position)
                if new_position in targets:
                    best_moves.append((move, length, new_position))
                    run = False
                    continue
                new_tiles = [new_position +
                             direction for direction in MOVE_DIRECTIONS]
                new_stack += [new_tile
                              for new_tile in new_tiles
                              if new_tile not in seen_positions and new_tile not in invalid_positions]
            stack = list(new_stack)
            if not stack:
                run = False
    if not best_moves:
        return -1
    min_length = min([x[1] for x in best_moves])
    best_moves = [x for x in best_moves if x[1] == min_length]
    best_moves.sort(key=lambda x: (-x[2].imag,
                                   x[2].real, -x[0].imag, x[0].real))
    return best_moves[0][0]


def make_unit_turn(unit_position: Position, mates: Team, enemies: Team, walls: Walls, attack_power: int) -> Position:
    if attack(unit_position, enemies, attack_power):
        return unit_position
    attack_positions = get_attack_positions(mates, enemies, walls)
    whole_map = [*mates.keys(), *enemies.keys(), *walls]
    new_position = get_move(unit_position, attack_positions, whole_map)
    if new_position != -1:
        hit_points = mates[unit_position]
        del mates[unit_position]
        mates[new_position] = hit_points
        attack(new_position, enemies, attack_power)
        return new_position

    return unit_position


DEFAULT_POWER = 3


def make_round(walls: Walls, elves: Team, goblins: Team, elf_power: int) -> bool:
    units_to_play = sorted([*elves, *goblins],
                           key=lambda p: (-p.imag, p.real))
    new_positions: List[Position] = []
    while units_to_play:
        position = units_to_play.pop(0)
        if position in new_positions:
            continue
        if position in goblins:
            if not elves:
                return False
            new_positions.append(make_unit_turn(
                position, goblins, elves, walls, DEFAULT_POWER))
        elif position in elves:
            if not goblins:
                return False
            new_positions.append(make_unit_turn(
                position, elves, goblins, walls, elf_power))
    return True


def run_game(walls: Walls, elves: Team, goblins: Team, all_elves: bool, elfPower: int = DEFAULT_POWER) -> Tuple[bool, int]:
    elves = dict(elves)
    starting_elves = len(elves)
    goblins = dict(goblins)
    round = 0
    while make_round(walls, elves, goblins, elfPower) and not (all_elves and len(elves) != starting_elves):
        round += 1
    return len(elves) == starting_elves, round * (sum(elves.values()) + sum(goblins.values()))


def part1(game: Tuple[Walls, Team, Team]) -> int:
    walls, elves, goblins = game
    _, result = run_game(walls, elves, goblins, False)
    return result


def part2(game: Tuple[Walls, Team, Team]) -> int:
    walls, elves, goblins = game
    elf_power = 10
    while True:
        elf_power += 1
        success, result = run_game(walls, elves, goblins, True, elf_power)
        if success:
            return result


def solve(game: Tuple[Walls, Team, Team]) -> Tuple[int, int]:
    return (
        part1(game),
        part2(game)
    )


def get_input(file_path: str) -> Tuple[Walls, Team, Team]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        walls: List[Position] = []
        elves: Dict[Position, int] = {}
        goblins: Dict[Position, int] = {}
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

    start = time.perf_counter()
    part1_result, part2_result = solve(get_input(sys.argv[1]))
    end = time.perf_counter()
    print("P1:", part1_result)
    print("P2:", part2_result)
    print()
    print(f"Time: {end - start:.7f}")


if __name__ == "__main__":
    main()
