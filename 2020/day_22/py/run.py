#! /usr/bin/python3

import sys, os, time


class Player():
    def __init__(self, name, cards):
        self.name = name
        self.cards = cards
        self.previousHands = [ ] 
        self.lastCard = None

    @staticmethod
    def fromLines(lines):
        name, *cards = lines.split("\n")
        name = name.replace("Player", "").replace(":", "").strip()
        cards = [ c for c in cards if c ]
        return Player(name, list(map(lambda i: int(i.strip()), cards)))

    def __str__(self):
        return f"Player {self.name}: {self.cards}"

    def getTopCard(self):
        self.previousHands.append(set(self.cards))
        self.lastCard = self.cards.pop(0)
        return self.lastCard

    def addCards(self, cards):
        self.cards += cards

    def hasRepeatedHand(self):
        return set(self.cards) in self.previousHands

    def clone(self, keepState = False):
        if keepState:
            return Player(self.name, list(self.cards[:self.lastCard]))
        return Player(self.name, list(self.cards))
    
    def getScore(self):
        worth = 1
        result = 0
        for card in self.cards[::-1]:
            result += card * worth
            worth += 1
        return result


def getPlayersFromInput(puzzleInput):
    player1, player2 = puzzleInput
    return player1.clone(), player2.clone()


def part1(puzzleInput):
    player1, player2 = getPlayersFromInput(puzzleInput)
    while len(player1.cards) and len(player2.cards):
        player1Card = player1.getTopCard()
        player2Card = player2.getTopCard()
        if player1Card > player2Card:
            player1.addCards([player1Card, player2Card])
        else:
            player2.addCards([player2Card, player1Card])

    winner = player1 if len(player1.cards) else player2
    return winner.getScore()


def decideRound(player1, player2):
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


def playGame(player1, player2):
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


def part2(puzzleInput):
    player1, player2 = getPlayersFromInput(puzzleInput)
    winner = playGame(player1, player2)
    return winner.getScore()


def getInput(filePath):
    if not os.path.isfile(filePath):
        raise FileNotFoundError(filePath)
    
    with open(filePath, "r") as file:
        contents = file.read()
        players = contents.split("\n\n")
        return Player.fromLines(players[0]), Player.fromLines(players[1])


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