#! /usr/bin/python3

from common import getInput


def main():
    player1, player2 = getInput()
    while len(player1.cards) and len(player2.cards):
        player1Card = player1.getTopCard()
        player2Card = player2.getTopCard()
        if player1Card > player2Card:
            player1.addCards([player1Card, player2Card])
        else:
            player2.addCards([player2Card, player1Card])

    winner = player1 if len(player1.cards) else player2
    worth = 1
    result = 0
    for card in winner.cards[::-1]:
        result += card * worth
        worth += 1
    print("Winning player's score:", result)


if __name__ == "__main__":
    main()
