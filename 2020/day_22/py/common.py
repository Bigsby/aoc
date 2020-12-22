import sys, os


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

    def clone(self):
        return Player(self.name, list(self.cards[:self.lastCard]))
        
        

def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        contents = file.read()
        players = contents.split("\n\n")
        return Player.fromLines(players[0]), Player.fromLines(players[1])
