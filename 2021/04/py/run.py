#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Card = List[List[int]]
Input = (List[int], List[Card])

def copy_cards(cards: List[Card]) -> List[Card]:
    result = []
    for card in cards:
        copy = list()
        for row in card:
            copy.append(list(row))
        result.append(copy)
    return result


def is_card_complete(card: Card) -> bool:
    for x in range(5):
        x_complete = True
        y_complete = True
        for y in range(5):
            x_complete &= card[x][y] < 0
            y_complete &= card[y][x] < 0
        if x_complete or y_complete:
            return True
    return False


def get_card_unmarked_sum(card: Card) -> int:
    return sum(map(lambda row: sum([ card_number for card_number in row if card_number > 0]), card))


def play_game(puzzle_input: Input, first: bool) -> int:
    numbers, cards = puzzle_input
    cards = copy_cards(cards)
    for number in numbers:
        to_remove = []
        for card in cards:
            for row in card:
                if number in row:
                    row[row.index(number)] = -100
                    if is_card_complete(card):
                        if first:
                            return get_card_unmarked_sum(card) * number
                        to_remove.append(card)
        for card in to_remove:
            cards.remove(card)
            if len(cards) == 0:
                return get_card_unmarked_sum(card) * number


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (play_game(puzzle_input, True), play_game(puzzle_input, False))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    
    with open(file_path) as file:
        numbers = []
        first_line = True
        cards = []
        card_row = -2
        card = []
        for line in file.readlines():
            if first_line:
                first_line = False
                numbers = [ int(number) for number in line.split(',') ]
            else:
                card_row += 1
                if card_row == -1:
                    continue
                card.append([ int(number) for number in line.strip().split(' ') if number ])
                if card_row == 4:
                    cards.append(card)
                    card = []
                    card_row = -2

        return numbers, cards 


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
