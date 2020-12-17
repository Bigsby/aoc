#! /usr/bin/python3

from common import getInput, Dimension


def main():
    cube = getInput()
    print(cube)
    cycle = 0
    while cycle < 6:
        cycle += 1
        cube = cube.getNextStep()
    activeCount = cube.getActiveCount()
    print("Active cubes:", activeCount)




if __name__ == "__main__":
    main()
