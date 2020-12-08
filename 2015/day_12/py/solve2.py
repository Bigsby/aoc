#! /usr/bin/python3

import json
from functools import reduce

from common import getInput


def getTotal(obj):
    if isinstance(obj, dict):
        if any(filter(lambda key: obj[key] == "red", obj.keys())):
            return 0
        return reduce(lambda total, key: total + getTotal(obj[key]), obj.keys(), 0)
    if isinstance(obj, int):
        return int(obj)
    if isinstance(obj, list):
        return reduce(lambda total, item: total + getTotal(item), obj, 0)
    return 0


def main():
    report = json.loads(getInput())
    total = getTotal(report)
    print("Total:", total)



if __name__ == "__main__":
    main()
