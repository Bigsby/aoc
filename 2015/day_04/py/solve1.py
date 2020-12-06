#! /usr/bin/python3

from hashlib import md5

from common import getInput


def main():
    key = getInput()
    guess = 1
    while True:
        result = md5((key + str(guess)).encode("utf-8")).hexdigest()
        if result.startswith("00000"):
            break
        guess = guess + 1

    print("Hash is:", guess)


if __name__ == "__main__":
    main()
