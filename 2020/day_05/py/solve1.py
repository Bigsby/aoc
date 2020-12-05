#! /usr/bin/python3

from common import getInput


def main():
    highestId = max(map(lambda boardingPass: boardingPass.id, getInput()))
    print("Highest Id is", highestId)
    

if __name__ == "__main__":
    main()
