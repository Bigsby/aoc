#! /usr/bin/python3

import sys
import os
import time
from typing import List, Set, Tuple


class Player():
    def __init__(self, name: str, cards: List[int]):
        self.name = name
        self.cards = cards
        self.previous_hands: List[Set[int]] = []
        self.last_card = 0

    @staticmethod
    def from_lines(lines: str) -> 'Player':
        name, *cards = lines.split("\n")
        name = name.replace("Player", "").replace(":", "").strip()
        cards = [c for c in cards if c]
        return Player(name, list(map(lambda i: int(i.strip()), cards)))

    def __str__(self) -> str:
        return f"number {self.name}: cards {self.cards}"

    def get_top_card(self) -> int:
        self.previous_hands.append(set(self.cards))
        self.last_card = self.cards.pop(0)
        return self.last_card

    def add_cards(self, cards: List[int]):
        self.cards += cards

    def has_repeated_hand(self) -> bool:
        return set(self.cards) in self.previous_hands

    def clone(self, keep_state: bool = False) -> 'Player':
        if keep_state:
            return Player(self.name, list(self.cards[:self.last_card]))
        return Player(self.name, list(self.cards))

    def get_score(self) -> int:
        worth = 1
        result = 0
        for card in self.cards[::-1]:
            result += card * worth
            worth += 1
        return result


def get_players_from_input(players: Tuple[Player, Player]) -> Tuple[Player, Player]:
    player1, player2 = players
    return player1.clone(), player2.clone()


def part1(players: Tuple[Player, Player]) -> int:
    player1, player2 = get_players_from_input(players)
    while len(player1.cards) and len(player2.cards):
        player1_card = player1.get_top_card()
        player2_card = player2.get_top_card()
        if player1_card > player2_card:
            player1.add_cards([player1_card, player2_card])
        else:
            player2.add_cards([player2_card, player1_card])
    winner = player1 if len(player1.cards) else player2
    return winner.get_score()


def decide_round(player1: Player, player2: Player) -> Tuple[Player, Player]:
    if all(player.last_card <= len(player.cards) for player in [player1, player2]):
        winner = play_game(player1.clone(True), player2.clone(True))
        if winner.name == player1.name:
            return player1, player2
        else:
            return player2, player1
    else:
        if player1.last_card > player2.last_card:
            return player1, player2
        else:
            return player2, player1


def play_game(player1: Player, player2: Player) -> Player:
    while len(player1.cards) and len(player2.cards):
        if player1.has_repeated_hand() or player2.has_repeated_hand():
            return player1
        player1.get_top_card()
        player2.get_top_card()
        winner, looser = decide_round(player1, player2)
        winner.add_cards([winner.last_card, looser.last_card])

    if len(player1.cards):
        return player1
    else:
        return player2


def part2(players: Tuple[Player, Player]) -> int:
    player1, player2 = get_players_from_input(players)
    winner = play_game(player1, player2)
    return winner.get_score()


def solve(players: Tuple[Player, Player]) -> Tuple[int, int]:
    return (
        part1(players),
        part2(players)
    )


def get_input(file_path: str) -> Tuple[Player, Player]:
    if not os.path.isfile(file_path):
        raise FileNotFoundError(file_path)

    with open(file_path, "r") as file:
        contents = file.read()
        players = contents.split("\n\n")
        return Player.from_lines(players[0]), Player.from_lines(players[1])


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
