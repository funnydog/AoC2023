#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = f.read().strip().split()
    except:
        print(f"cannot open { sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    galaxies = []
    for y, row in enumerate(lines):
        for x, value in enumerate(row):
            if value == "#":
                galaxies.append((x, y))

    # find empty rows and columns
    empty_rows = []
    empty_row = "." * len(lines[0])
    for y, row in enumerate(lines):
        if row == empty_row:
            empty_rows.append(y)

    empty_columns = []
    for x in range(len(lines[0])):
        for y in range(len(lines)):
            if lines[y][x] == "#":
                break
        else:
            empty_columns.append(x)

    # adjust the galaxy coordinates
    def expand(e):
        e -= 1
        ngalaxies = []
        for gx, gy in galaxies:
            gy += sum(e for y in empty_rows if gy > y)
            gx += sum(e for x in empty_columns if gx > x)
            ngalaxies.append((gx, gy))
        return ngalaxies

    def distance(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0]-b[0]) + abs(a[1]-b[1])

    def sum_distances(galaxies):
        dsum = 0
        for i in range(len(galaxies)):
            for j in range(i+1, len(galaxies)):
                dsum += distance(galaxies[i], galaxies[j])
        return dsum

    print("Part1:", sum_distances(expand(2)))
    print("Part2:", sum_distances(expand(1000000)))
