#! /usr/bin/python3

from common import getInput, moves

keypad = [
   [ "1", "2", "3" ],
   [ "4", "5", "6" ],
   [ "7", "8", "9" ]
]


def getNewPosition(current, move):
    step = moves[move]
    newPosition = (current[0] + step[0], current[1] + step[1])
    if newPosition[0] < 0 or newPosition[0] > 2 or newPosition[1] < 0 or newPosition[1] > 2:
        return current
    return newPosition


def main():
    buttons = list(getInput())
    currentPosition = (1,1)
    code = []
    for button in buttons:
        for move in button:
            currentPosition = getNewPosition(currentPosition, move)

        code.append(keypad[currentPosition[0]][currentPosition[1]])


    result = "".join(code)
    print("Code:", result)

            



if __name__ == "__main__":
    main()
