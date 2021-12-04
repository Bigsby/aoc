#! /usr/bin/python3

import sys, os, time
from typing import Tuple, List

Card = List[List[int]]
Input = (List[int], List[Card])

def copyCards(cards: List[Card]) -> List[Card]:
    result = []
    for card in cards:
        copy = list()
        for row in card:
            copy.append(list(row))
        result.append(copy)
    return result


def isCardComplete(card: Card) -> bool:
    for row in range(5):
        rowComplete = True
        for column in range(5):
            rowComplete &= card[row][column] < 0
        if rowComplete:
            return True
    for column in range(5):
        columnComplete = True
        for row in range(5):
            columnComplete &= card[row][column] < 0
        if columnComplete:
            return True
    return False


def getCardUnmarkedSum(card: Card) -> int:
    return sum(map(lambda row: sum([ cardNumber for cardNumber in row if cardNumber > 0]), card))


def playGame(puzzle_input: Input, first: bool) -> int:
    numbers, cards = puzzle_input
    cards = copyCards(cards)
    for number in numbers:
        toRemove = []
        for card in cards:
            for row in card:
                if number in row:
                    row[row.index(number)] = -100
                    if isCardComplete(card):
                        if first:
                            return getCardUnmarkedSum(card) * number
                        toRemove.append(card)
        for card in toRemove:
            cards.remove(card)
            if len(cards) == 0:
                return getCardUnmarkedSum(card) * number


def solve(puzzle_input: Input) -> Tuple[int,int]:
    return (playGame(puzzle_input, True), playGame(puzzle_input, False))


def get_input(file_path: str) -> Input:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)
    numbers = []
    firstLine = True
    cards = []
    
    with open(file_path) as file:
        numbers = []
        firstLine = True
        cards = []
        cardRow = 0
        card = []
        for line in file.readlines():
            if firstLine:
                firstLine = False
                numbers = [ int(number) for number in line.split(',') ]
            else:
                cardRow += 1
                if cardRow == 1:
                    continue
                card.append([ int(number) for number in line.strip().split(' ') if number ])
                if cardRow == 6:
                    cards.append(card)
                    card = []
                    cardRow = 0

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
