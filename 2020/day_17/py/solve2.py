#! /usr/bin/python3

from common import getInput, Dimension


def main():
    universe = getInput(True)
    print(universe)
    cycle = 0
    while cycle < 6:
        cycle += 1
        universe = universe.getNextStep()
    activeCount = universe.getActiveCount()
    print("Active cubes:", activeCount)




if __name__ == "__main__":
    main()
