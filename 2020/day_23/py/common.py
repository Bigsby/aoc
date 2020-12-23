import sys, os


debug = True


class Node:
    def __init__(self, value):
        self.next = None
        self.value = value
    def __str__(self):
        return f"{self.value} > {self.next.value if self.next else 0}"


def getInput():
    if len(sys.argv) != 2:
        print("Please, add input file path as parameter")
        sys.exit(1)

    filePath = sys.argv[1]
    if not os.path.isfile(filePath):
        print("File not found")
        sys.exit(1)

    with open(filePath, "r") as file:
        for c in file.read().strip():
            yield int(c)


def buildLinkedList(cups):
    start = previous = last = Node(cups[0])
    values = [None] * len(cups)
    values[start.value - 1] = start
    for cup in cups[1:]:
        last = Node(cup)
        previous.next = last
        values[last.value - 1] = last
        previous = last
    last.next = start
    return start, values


def playGame(cups, moves):
    global debug
    move = 0
    start, values = buildLinkedList(cups)
    maxValue = max(cups)
    current = start


    while move < moves:
        move += 1
        firstRemoved = current.next
        lastRemoved = firstRemoved.next.next
        removedValues = {firstRemoved.value, firstRemoved.next.value, lastRemoved.value}
        current.next = lastRemoved.next

        destinationValue = current.value - 1
        while destinationValue in removedValues or destinationValue < 1:
            destinationValue -= 1
            if destinationValue < 0:
                destinationValue = maxValue
        destinationLink = values[destinationValue - 1]
        lastRemoved.next = destinationLink.next
        destinationLink.next = firstRemoved

        current = current.next
    return values[0]
