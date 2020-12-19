#! /usr/bin/python3
import re
from functools import reduce

from common import getInput, generateRegex

def isInnerMatch(rule, message, position):
    match = re.match(rule, message[position:])
    if match:
        return True, position + match.end()
    return False, position

  
def isMatch(firstRule, secondRule, message):
    count = 0
    matched, position = isInnerMatch(firstRule, message, 0)
    while matched and position <= len(message):
        lastPosition = position
        for _ in range(count):
            matched, position = isInnerMatch(secondRule, message, position)
            if not matched:  
                position = lastPosition
                break
            elif position == len(message):  
                return True

        count += 1
        matched, position = isInnerMatch(firstRule, message, position)
    return False


def main():
    rules, messages = getInput()

    rule42 = generateRegex(rules, 42)
    rule31 = generateRegex(rules, 31)

    count = reduce(lambda soFar, message: soFar + isMatch(rule42, rule31, message), messages, 0)
    print("Zero rule matches:", count)




if __name__ == "__main__":
    main()
