#! /usr/bin/python3

from common import getInput, moves


keypad = [
    [ "0", "0", "1", "0", "0" ],
    [ "0", "2", "3", "4", "0" ],
    [ "5", "6", "7", "8", "9" ],
    [ "0", "A", "B", "C", "0" ],
    [ "0", "0", "D", "0", "0" ]
]

def getNewPosition(current, move):
    step = moves[move]
    newPosition = (current[0] + step[0], current[1] + step[1])
    if newPosition[0] < 0 or newPosition[0] > 4 or newPosition[1] < 0 or newPosition[1] > 4 or keypad[newPosition[0]][newPosition[1]] == "0":
        return current
    return newPosition
 

def main():
    buttons = list(getInput())
    currentPosition = (2,0)
    code = []
    for button in buttons:
        for move in button:
            currentPosition = getNewPosition(currentPosition, move)

        code.append(keypad[currentPosition[0]][currentPosition[1]])


    result = "".join(code)
    print("Code:", result)



if __name__ == "__main__":
    main()
