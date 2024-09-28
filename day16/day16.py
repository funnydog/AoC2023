#!/usr/bin/env python3
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = f.read().strip().splitlines()
    except:
        print(f"cannot open { sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    height, width = len(lines), len(lines[0])

    NORTH, WEST, SOUTH, EAST = 0, 1, 2, 3
    def update(x, y, d):
        if d == NORTH:
            return (x, y-1, d)
        elif d == WEST:
            return (x-1, y, d)
        elif d == SOUTH:
            return (x, y+1, d)
        elif d == EAST:
            return (x+1, y, d)
        else:
            exit(1)

    def count_energized(x, y, direction):
        energized = [[0 for x in row] for row in lines]
        queue = [(x, y, direction)]
        while queue:
            x, y, d = queue.pop()

            if x < 0 or x >= width or y < 0 or y >= height:
                continue

            if energized[y][x] & 1 << d:
                continue

            energized[y][x] |= 1 << d
            t = lines[y][x]
            if t == ".":
                queue.append(update(x, y, d))
            elif t == "\\":
                if d == NORTH:
                    d = WEST
                elif d == WEST:
                    d = NORTH
                elif d == SOUTH:
                    d = EAST
                elif d == EAST:
                    d = SOUTH
                queue.append(update(x, y, d))
            elif t == "/":
                if d == NORTH:
                    d = EAST
                elif d == WEST:
                    d = SOUTH
                elif d == SOUTH:
                    d = WEST
                elif d == EAST:
                    d = NORTH
                queue.append(update(x, y, d))
            elif t == "-":
                if d == WEST or d == EAST:
                    queue.append(update(x, y, d))
                else:
                    queue.append(update(x, y, WEST))
                    queue.append(update(x, y, EAST))
            elif t == "|":
                if d == NORTH or d == SOUTH:
                    queue.append(update(x, y, d))
                else:
                    queue.append(update(x, y, NORTH))
                    queue.append(update(x, y, SOUTH))

        count = 0
        for y, row in enumerate(energized):
            for x, v in enumerate(row):
                if v:
                    count += 1
        return count

    print("Part1:", count_energized(0, 0, EAST))

    maxe = 0
    for y in range(height):
        e = count_energized(0, y, EAST)
        if maxe < e:
            maxe = e
        e = count_energized(width-1, y, WEST)
        if maxe < e:
            maxe = e

    for x in range(width):
        e = count_energized(x, 0, SOUTH)
        if maxe < e:
            maxe = e
        e = count_energized(x, height-1, NORTH)
        if maxe < e:
            maxe = e
    print("Part2:", maxe)
