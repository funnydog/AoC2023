#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    with open(sys.argv[1], "rt") as f:
        lines = f.readlines()

    height, width = len(lines), len(lines[0])
    def append_symbol(symbols, nx, ny):
        if 0 <= nx < width and 0 <= ny < height:
            value = lines[ny][nx]
            if value not in "0123456789.\n":
                symbols.append((nx, ny))
        return symbols

    numbers, stars = [], []
    number, symbols = "", []
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            if char in "0123456789":
                if not number:
                    symbols = append_symbol(symbols, x-1, y-1)
                    symbols = append_symbol(symbols, x-1, y)
                    symbols = append_symbol(symbols, x-1, y+1)
                symbols = append_symbol(symbols, x, y-1)
                symbols = append_symbol(symbols, x, y+1)
                number += char
            else:
                if number:
                    symbols = append_symbol(symbols, x, y-1)
                    symbols = append_symbol(symbols, x, y)
                    symbols = append_symbol(symbols, x, y+1)
                    if symbols:
                        numbers.append((int(number), symbols))
                number, symbols = "", []
            if char == "*":
                stars.append((x, y))

    part1 = 0
    for number, symbols in numbers:
        if symbols:
            part1 += number

    part2 = 0
    for star in stars:
        values = []
        for number, symbols in numbers:
            if star in symbols:
                values.append(number)

        if len(values) > 1:
            part2 += values[0] * values[1]

    print("Part1:", part1)
    print("Part2:", part2)
