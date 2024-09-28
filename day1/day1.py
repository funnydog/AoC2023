#!/usr/bin/env python

digits = "0123456789"
spelled_out_digits = (
    "zero",
    "one",
    "two",
    "three",
    "four",
    "five",
    "six",
    "seven",
    "eight",
    "nine"
)

def check1(line, pos):
    global digits
    if line[pos] in digits:
        return line[pos]
    return None

def check2(line, pos):
    global digits, spelled_out_digits
    value = check1(line, pos)
    if value:
        return value

    for j, digit in enumerate(spelled_out_digits):
        if line.startswith(digit, pos):
            return digits[j]

    return None

def decode(line, checkfn):
    first, last = None, None
    for i in range(len(line)):
        value = checkfn(line, i)
        if value:
            if not first:
                first = value
            last = value

    return int(first + last)

import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        lines = f.readlines()

    print("Part1:", sum(decode(line, check1) for line in lines))
    print("Part2:", sum(decode(line, check2) for line in lines))
