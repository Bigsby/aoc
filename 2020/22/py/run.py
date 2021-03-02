#! /usr/bin/python3

import sys, os, time
from typing import List, Tuple


class Player():
    def __init__(self, name: str, cards: List[int]):
        self.name = name
        self.cards = cards
        self.previousHands = [ ] 
        self.lastCard = 0

    @staticmethod
    def fromLines(lines: str) -> 'Player':
        name, *cards = lines.split("\n")
        name = name.replace("Player", "").replace(":", "").strip()
        cards = [ c for c in cards if c ]
        return Player(name, list(map(lambda i: int(i.strip()), cards)))

    def __str__(self) -> str:
        return f"Player {self.name}: {self.cards}"

    def getTopCard(self) -> int:
        self.previousHands.append(set(self.cards))
        self.lastCard = self.cards.pop(0)
        return self.lastCard

    def addCards(self, cards: List[int]):
        self.cards += cards

    def hasRepeatedHand(self) -> bool:
        return set(self.cards) in self.previousHands

    def clone(self, keepState: bool  = False) -> 'Player':
        if keepState:
            return Player(self.name, list(self.cards[:self.lastCard]))
        return Player(self.name, list(self.cards))
    
    def getScore(self) -> int:
        worth = 1
        result = 0
        for card in self.cards[::-1]:
            result += card * worth
            worth += 1
        return result


def getPlayersFromInput(players: Tuple[Player,Player]) -> Tuple[Player,Player]:
    player1, player2 = players
    return player1.clone(), player2.clone()


def part1(players: Tuple[Player,Player]) -> int:
    player1, player2 = getPlayersFromInput(players)
    while len(player1.cards) and len(player2.cards):
        player1Card = player1.getTopCard()
        player2Card = player2.getTopCard()
        if player1Card > player2Card:
            player1.addCards([player1Card, player2Card])
        else:
            player2.addCards([player2Card, player1Card])
    winner = player1 if len(player1.cards) else player2
    return winner.getScore()


def decideRound(player1: Player, player2: Player) -> Tuple[Player,Player]:
    if all(player.lastCard <= len(player.cards) for player in [player1, player2]):
        winner = playGame(player1.clone(True), player2.clone(True))
        if winner.name == player1.name:
            return player1, player2
        else:
            return player2, player1
    else:
        if player1.lastCard > player2.lastCard:
            return player1, player2
        else:
            return player2, player1


def playGame(player1: Player, player2: Player) -> Player:
    while len(player1.cards) and len(player2.cards):
        if player1.hasRepeatedHand() or player2.hasRepeatedHand():
            return player1
        player1.getTopCard()
        player2.getTopCard()
        winner, looser = decideRound(player1, player2)
        winner.addCards([winner.lastCard, looser.lastCard])

    if len(player1.cards):
        return player1
    else:
        return player2


def part2(players: Tuple[Player,Player]) -> int:
    player1, player2 = getPlayersFromInput(players)
    winner = playGame(player1, player2)
    return winner.getScore()


def solve(players: Tuple[Player,Player]) -> Tuple[int,int]:
    return (
        part1(players),
        part2(players)
    )


def getInput(filePath: str) -> Tuple[Player,Player]:
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        contents = file.read()
        players = contents.split("\n\n")
        return Player.fromLines(players[0]), Player.fromLines(players[1])


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