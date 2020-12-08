#! /usr/bin/python3

from common import getInput, getNextValidPassword
       

def main():
    currentPassword = getInput()
    nextValidPassword = getNextValidPassword(currentPassword)
    print("Next password:", nextValidPassword)


if __name__ == "__main__":
    main()
