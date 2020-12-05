#! /usr/bin/python3

from common import getInput


def main():
    boardingPasses = sorted(getInput(), key=lambda bp: bp.id)
    mySeatId = boardingPasses[0].id
    for bp in boardingPasses:
        if bp.id - mySeatId == 2:
            break
        mySeatId = bp.id

    print("My seat Id:", mySeatId + 1)


if __name__ == "__main__":
    main()
