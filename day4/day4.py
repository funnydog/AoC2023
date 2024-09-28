#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        lines = f.readlines()

    cards_count = [1 for i in lines]
    part1 = 0
    for i, line in enumerate(lines):
        card, numbers = line.split(":")
        win, own = numbers.strip().split("|")

        win_numbers = set(int(x) for x in win.split())
        own_numbers = [int(x) for x in own.split()]

        count = 0
        for number in own_numbers:
            if number in win_numbers:
                count += 1

        if count:
            part1 += 1 << (count - 1)

        for j in range(i+1, i+1+count):
            if j < len(cards_count):
                cards_count[j] += cards_count[i]

    print("Part1:", part1)
    print("Part2:", sum(cards_count))
