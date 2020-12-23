#! /usr/bin/python3

from common import getInput, playGame


def main():
    cups = list(getInput())

    oneNode = playGame(cups, 100)
    result = []
    currentNode = oneNode.next
    while currentNode.value != 1:
        result.append(currentNode.value)
        currentNode = currentNode.next

    print("Result:", "".join(map(str, result)))

if __name__ == "__main__":
    main()
