#! /usr/bin/python3
import sys
import os
import time
from typing import Dict, Iterable, List, Tuple
import re
from functools import reduce
from math import sqrt

Tile = List[complex]


def get_size(tile: Tile, height: bool = False) -> int:
    if height:
        return int(max(map(lambda value: value.imag, tile)))
    return int(max(map(lambda value: value.real, tile)))


def print_tile(tile: Tile):
    start_x = int(min(map(lambda value: value.imag, tile)))
    end_x = int(max(map(lambda value: value.imag, tile)))
    start_y = int(min(map(lambda value: value.real, tile)))
    end_y = int(max(map(lambda value: value.real, tile)))
    for row in range(start_x, end_x + 1):
        for column in range(start_y, end_y + 1):
            position = column + row * 1j
            print("#" if position in tile else ".", end="")
        print()
    print()


def mirror_horizontal(tile: Tile, size: int) -> Tile:
    return [position.imag * 1j + size - position.real for position in tile]


def rotate_clockwise(tile: Tile, size: int) -> Tile:
    return [position.real * 1j + size - position.imag for position in tile]


def generate_permutations(tile: Tile) -> Iterable[Tile]:
    size = get_size(tile)
    for _ in range(4):
        yield tile
        yield mirror_horizontal(tile, size)
        tile = rotate_clockwise(tile, size)


def generate_all_tiles_permutations(tiles: List[Tuple[int, Tile]]) -> Dict[int, List[Tile]]:
    return {number: list(generate_permutations(tile)) for number, tile in tiles}


TESTS = {  # ( startOfTileA, StartOfTileB, StepToNextPosition )
    -1j: (0, 1j, 1),  # match top with bottom left to right
    1: (1,  0, 1j),  # match right with left top to bottom
    1j: (1j,  0, 1),  # match bottom with top left to right
    -1: (0,  1, 1j)  # mathc left with right top to bottom
}


def test_sides(tile_a: Tile, tile_b: Tile, side: complex, size: int) -> bool:
    position_a_start, position_b_start, step = TESTS[side]
    position_a = position_a_start * size
    position_b = position_b_start * size
    for _ in range(size + 1):
        if (position_a in tile_a) ^ (position_b in tile_b):
            return False
        position_a += step
        position_b += step
    return True


def do_permutations_match(permutation_a: Tile, permutation_b: Tile, size: int, sides: List[complex]) -> Tuple[bool, complex]:
    for side in sides:
        if test_sides(permutation_a, permutation_b, side, size):
            return True, side
    return False, 0


def do_tiles_match(tile_a: Tile, permutations: List[Tile], size: int, sides: List[complex] = list(TESTS.keys())) -> Tuple[bool, complex, Tile]:
    for permutation in permutations:
        matched, side = do_permutations_match(tile_a, permutation, size, sides)
        if matched:
            return True, side, permutation
    return False, 0, []


def get_matching_sides(tile: Tuple[int, Tile], tiles: List[Tuple[int, Tile]], size: int, all_permutations: Dict[int, List[Tile]]) -> List[complex]:
    number, this_tile = tile
    matched_sides: List[complex] = []
    for other_number, _ in tiles:
        if other_number == number:
            continue
        matched, side, _ = do_tiles_match(
            this_tile, all_permutations[other_number], size)
        if matched:
            matched_sides.append(side)
    return matched_sides


def get_corners(tiles: List[Tuple[int, Tile]], size: int, all_permutations: Dict[int, List[Tile]]) -> List[Tuple[int, List[complex]]]:
    tiles_matched_sides = {number: get_matching_sides(
        (number, tile), tiles, size, all_permutations) for number, tile in tiles}
    return [(number, matched_sides) for number, matched_sides in tiles_matched_sides.items() if len(matched_sides) == 2]


def build_puzzle(tiles: List[Tuple[int, Tile]], tile_size: int, tile_permutations: Dict[int, List[Tile]], corners: List[Tuple[int, Tile]]) -> Dict[complex, Tile]:
    first_corner_number, (side_one, side_two) = corners[0]
    puzzle_width = int(sqrt(len(tiles)))
    puzzle_position = (puzzle_width - 1) * ((1 if side_one == -1 or side_two == -
                                             1 else 0) + (1j if side_one == -1j or side_two == -1j else 0))
    last_tile = tile_permutations[first_corner_number][0]
    del tile_permutations[first_corner_number]
    puzzle: Dict[complex, Tile] = {}
    puzzle[puzzle_position] = last_tile
    direction = side_one
    while tile_permutations:
        puzzle_position += direction
        for tile_number, permutations in tile_permutations.items():
            matched, _, matched_permutation = do_tiles_match(
                last_tile, permutations, tile_size, [direction])
            if matched:
                puzzle[puzzle_position] = last_tile = matched_permutation
                del tile_permutations[tile_number]
                if direction == side_two:
                    direction = (-1 if (len(puzzle) // puzzle_width) %
                                 2 else 1) * side_one
                elif len(puzzle) % puzzle_width == 0:
                    direction = side_two
                break
    return puzzle


def remove_borders_and_join(puzzle: Dict[complex, Tile], tile_size: int) -> Tile:
    offset_factor = tile_size - 1
    reduced = []
    for puzzle_position, tile in puzzle.items():
        for position in tile:
            if position.real > 0 and position.real < tile_size and position.imag > 0 and position.imag < tile_size:
                reduced.append((puzzle_position.real * offset_factor + position.real - 1) + (
                    puzzle_position.imag * offset_factor + position.imag - 1) * 1j)
    return reduced


SEA_MONSTER = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]


def get_sea_monster() -> Tile:
    sea_monster: Tile = []
    for row_index, row in enumerate(SEA_MONSTER):
        for column_index, c in enumerate(row):
            if c == "#":
                sea_monster.append(column_index + row_index * 1j)
    return sea_monster


def is_monster_in_location(location: complex, puzzle: Tile, sea_monster: Tile) -> bool:
    for monster_position in sea_monster:
        if not location + monster_position in puzzle:
            return False
    return True


def get_sea_monster_count(puzzle: Tile, sea_monster: Tile) -> int:
    sea_monster_width = get_size(sea_monster) + 1
    sea_monster_height = get_size(sea_monster, True) + 1
    puzzle_size = get_size(puzzle) + 1
    for permutation in generate_permutations(puzzle):
        count = 0
        for puzzle_x in range(0, puzzle_size - sea_monster_width):
            for puzzle_y in range(0, puzzle_size - sea_monster_height):
                if is_monster_in_location(puzzle_x + puzzle_y * 1j, permutation, sea_monster):
                    count += 1
        if count:
            return count
    return 0


def part2(tiles: List[Tuple[int, Tile]], tile_size: int, tile_permutations: Dict[int, List[Tile]], corners: List[Tuple[int, Tile]]) -> int:
    puzzle = build_puzzle(tiles, tile_size, tile_permutations, corners)
    reduced = remove_borders_and_join(puzzle, tile_size)
    sea_monster = get_sea_monster()
    location_count = get_sea_monster_count(reduced, sea_monster)
    return len(reduced) - len(sea_monster) * location_count


def solve(tiles: List[Tuple[int, Tile]]) -> Tuple[int, int]:
    permutations = generate_all_tiles_permutations(tiles)
    size = get_size(tiles[0][1])
    corners = get_corners(tiles, size, permutations)
    return (
        int(reduce(lambda soFar, corner: soFar * corner[0], corners, 1)),
        part2(tiles, size, permutations, corners)
    )


number_line_regex = re.compile(r"^Tile\s(?P<number>\d+):$")


def get_input(file_path: str) -> List[Tuple[int, Tile]]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        tiles: List[Tuple[int, Tile]] = []
        tile_number = 0
        tile: Tile = []
        position = 0j
        for line in file.readlines():
            number_match = number_line_regex.match(line)
            if number_match:
                tile_number = int(number_match.group("number"))
                tile = []
                position = 0j
            elif line.strip() == "":
                tiles.append((tile_number, tile))
            else:
                for c in line.strip():
                    if c == "#":
                        tile.append(position)
                    position += 1
                position += 1j - position.real
        return tiles


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
