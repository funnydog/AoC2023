#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        lines = f.readlines()

    part1 = 0
    part2 = 0
    for line in lines:
        game, sets = line.split(":")
        red, green, blue = [], [], []
        for single_set in sets.split(";"):
            for extraction in single_set.split(","):
                num, color = extraction.split()
                if color == "red":
                    red.append(int(num))
                elif color == "green":
                    green.append(int(num))
                elif color == "blue":
                    blue.append(int(num))
                else:
                    continue

        maxred = max(red)
        maxgreen = max(green)
        maxblue = max(blue)

        if maxred <= 12 and maxgreen <= 13 and maxblue <= 14:
            part1 += int(game.split()[1])
        part2 += maxred * maxgreen * maxblue

    print("Part1:", part1)
    print("Part2:", part2)

