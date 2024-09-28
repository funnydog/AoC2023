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

    height, width = len(lines), len(lines[0])

    NORTH, SOUTH, EAST, WEST = 1, 2, 4, 8

    def get_tile_directions(x, y) -> int:
        if x < 0 or x >= width or y < 0 or y >= height:
            return 0
        t = lines[y][x]
        if t == "|":
            return NORTH | SOUTH
        elif t == "-":
            return WEST | EAST
        elif t == "L":
            return NORTH | EAST
        elif t == "J":
            return NORTH | WEST
        elif t == "7":
            return SOUTH | WEST
        elif t == "F":
            return SOUTH | EAST
        elif t == "S":
            value = 0
            if get_tile_directions(x-1, y) & EAST:
                value |= WEST
            if get_tile_directions(x+1, y) & WEST:
                value |= EAST
            if get_tile_directions(x, y-1) & SOUTH:
                value |= NORTH
            if get_tile_directions(x, y+1) & NORTH:
                value |= SOUTH
            return value
        else:
            return 0

    # find the starting point of the loop S
    sx, sy = -1, -1
    for y, row in enumerate(lines):
        for x, value in enumerate(row):
            if value == "S":
                sx, sy = x, y
                break

    # BFS search to find the distance of any point in the loop from S
    visited: dict[tuple[int,int], int] = {}
    visited[sx, sy] = 0
    queue = [(sx, sy, 0)]
    while queue:
        x, y, distance = queue.pop(0)

        adjacent: list[tuple[int,int]] = []
        directions = get_tile_directions(x, y)
        if directions & NORTH:
            adjacent.append((x, y-1))
        if directions & SOUTH:
            adjacent.append((x, y+1))
        if directions & EAST:
            adjacent.append((x+1, y))
        if directions & WEST:
            adjacent.append((x-1, y))

        distance += 1
        for nx, ny in adjacent:
            if 0 <= nx < width and 0 <= ny < height and not (nx, ny) in visited:
                visited[nx, ny] = distance
                queue.append((nx, ny, distance))

    print("Part1:", max(visited.values()))

    # raster scan to find if a point is inside the loop
    enclosed = 0
    for y in range(height):
        directions = 0
        for x in range(width):
            if (x, y) in visited:
                directions ^= get_tile_directions(x, y) & (NORTH | SOUTH)
            elif directions:
                enclosed += 1

    print("Part2:", enclosed)
