#! /usr/bin/python3

from common import getInput

def decideRound(player1, player2):
    if all(player.lastCard <= len(player.cards) for player in [player1, player2]):
        winner, looser = playGame(player1.clone(), player2.clone())
        if winner.name == player1.name:
            return player1, player2
        else:
            return player2, player1
    else:
        if player1.lastCard > player2.lastCard:
            return player1, player2
        else:
            return player2, player1


gameCount = 0
def playGame(player1, player2):
    global gameCount
    gameCount += 1
    currentGame = gameCount
    roundCount = 0 

    while len(player1.cards) and len(player2.cards):

        if player1.hasRepeatedHand() or player2.hasRepeatedHand():
            return player1, player2

        roundCount += 1

        player1Card = player1.getTopCard()
        player2Card = player2.getTopCard()

        winner, looser = decideRound(player1, player2)
        winner.addCards([winner.lastCard, looser.lastCard])

    if len(player1.cards):
        return player1, player2
    else:
        return player2, player2



def main():
    player1, player2 = getInput()
    winner, _ = playGame(player1, player2)
    worth = 1
    result = 0
    for card in winner.cards[::-1]:
        result += card * worth
        worth += 1
    print("Winning player's score:", result)


if __name__ == "__main__":
    main()
