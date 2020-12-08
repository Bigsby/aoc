#! /usr/bin/python3

from common import getInput, testBoot


def switchAndTest(op, ops):
    originaMnemonic = op.mnemonic
    op.mnemonic = "nop" if originaMnemonic == "jmp" else "nop"
    success, accumulator = testBoot(ops)
    op.mnemonic = originaMnemonic
    return success, accumulator


def main():
    ops = list(getInput())
    for index in range(0, len(ops)):
        op = ops[index]
        if op.mnemonic == "acc":
            continue
        success, accumulator = switchAndTest(op, ops)
        if success:
            print("Accumulator value:", accumulator)
            break


if __name__ == "__main__":
    main()
