#! /usr/bin/python3

from common import getInput, playGame

debug = False



def main():
    cups = list(getInput())

    cups = playGame(cups, 100)

    if debug:
        print("-- final --")
        print("cups:", " ".join(map(str, cups)))

    oneindex = cups.index(1)
    result = cups[oneindex + 1:] + cups[:oneindex]
    print("Result:", "".join(map(str, result)))

if __name__ == "__main__":
    main()
