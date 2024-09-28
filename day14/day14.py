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

    # convert the data to an assignable structure
    m = [list(line) for line in lines]
    height, width = len(m), len(m[0])

    NORTH, SOUTH, WEST, EAST = 0, 1, 2, 3

    def tilt(m, d):
        nm = [row[:] for row in m]
        dy = d == SOUTH and -1 or 1
        dx = d == EAST and -1 or 1

        y = d == SOUTH and height-1 or 0
        while 0 <= y < height:
            x = d == EAST and width-1 or 0
            while 0 <= x < width:
                tile = nm[y][x]
                if tile == "O":
                    nm[y][x] = "."
                    nx, ny = x, y
                    if d == NORTH:
                        while ny >= 0 and nm[ny][nx] == ".":
                            ny -= 1
                        ny += 1
                    elif d == SOUTH:
                        while ny < height and nm[ny][nx] == ".":
                            ny += 1
                        ny -= 1
                    elif d == WEST:
                        while 0 <= nx and nm[ny][nx] == ".":
                            nx -= 1
                        nx += 1
                    elif d == EAST:
                        while nx < width and nm[ny][nx] == ".":
                            nx += 1
                        nx -= 1
                    else:
                        print("Unknown direction", d, file=sys.stderr)
                        exit(1)
                    nm[ny][nx] = "O"
                x += dx
            y += dy
        return nm

    def points(m):
        p = 0
        for y, row in enumerate(m):
            rocks = 0
            for v in row:
                if v == "O":
                    rocks += 1

            p += rocks * (height - y)
        return p

    print("Part1:", points(tilt(m, NORTH)))

    def cycle(m):
        m = tilt(m, NORTH)
        m = tilt(m, WEST)
        m = tilt(m, SOUTH)
        m = tilt(m, EAST)
        return m

    def eq(a, b):
        for y, row in enumerate(a):
            if "".join(row) != "".join(b[y]):
                return False
        return True

    # Floyd's cycle detection algorithm
    t = cycle(m)
    h = cycle(cycle(m))
    while not eq(t, h):
        t = cycle(t)
        h = cycle(cycle(h))

    # remainder
    remainder = 0
    t = m
    while not eq(t, h):
        t = cycle(t)
        h = cycle(h)
        remainder += 1

    # modulus
    modulus = 1
    h = cycle(t)
    while not eq(t, h):
        h = cycle(h)
        modulus += 1

    count = (1000000000 - remainder) % modulus
    while count > 0:
        h = cycle(h)
        count -= 1

    print("Part2:", points(h))
