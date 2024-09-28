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

    def is_equal(ta: tuple[int,int], tb: tuple[int,int], distance) -> bool:
        ax, ay = ta[0] * width, ta[1] * height
        bx, by = tb[0] * width, tb[1] * height
        for x in range(width):
            a = distance.get((ax+x, ay), -1)
            b = distance.get((bx+x, by), -1)
            if a < 0 or b < 0 or a != b:
                return False

            a = distance.get((ax+x, ay+height-1), -1)
            b = distance.get((bx+x, by+height-1), -1)
            if a < 0 or b < 0 or a != b:
                return False

        for y in range(1, height-2):
            a = distance.get((ax, ay+y), -1)
            b = distance.get((bx, by+y), -1)
            if a < 0 or b < 0 or a != b:
                return False

            a = distance.get((ax+width-1, ay+y), -1)
            b = distance.get((bx+width-1, by+y), -1)
            if a < 0 or b < 0 or a != b:
                return False

        return True

    def bfs(sx, sy):
        queue = [(sx, sy, 0)]
        distance = {}
        x0, x1, y0, y1 = 0, 0, 0, 0
        while queue:
            x, y, steps = queue.pop(0)

            nsteps = steps + 1
            for dx, dy in (-1,0), (0,-1), (1,0), (0,1):
                nx = x + dx
                ny = y + dy

                # check against the boundaries
                if x0 and nx < x0 or x1 and nx >= x1: continue
                if y0 and ny < y0 or y1 and ny >= y1: continue

                tx, rx = nx // width, nx % width
                ty, ry = ny // height, ny % height

                # find the boundaries
                if tx == 0 or ty == 0:
                    if x1 == 0 and dx > 0 and rx == 0:
                        if is_equal((tx-1, ty), (tx-2, ty), distance):
                            x1 = x+1
                    if x0 == 0 and dx < 0 and rx == width-1:
                        if is_equal((tx+1, ty), (tx+2, ty), distance):
                            x0 = x
                    if y1 == 0 and dy > 0 and ry == 0:
                        if is_equal((tx, ty-1), (tx, ty-2), distance):
                            y1 = y+1
                    if y0 == 0 and dy < 0 and ry == height-1:
                        if is_equal((tx, ty+1), (tx, ty+2), distance):
                            y0 = y

                if lines[ry][rx] != "#" and not (nx, ny) in distance:
                    distance[nx, ny] = nsteps - abs(nx-sx) - abs(ny-sy)
                    queue.append((nx, ny, nsteps))

        return distance, ((x0, y0), (x1, y1))

    # find the start position
    sx, sy = 0, 0
    for y, row in enumerate(lines):
        for x, tile in enumerate(row):
            if tile == "S":
                sx, sy = x, y
                break

    ndistance, nrect = bfs(sx, sy)

    def get_value(x, y):
        (x0, y0), (x1, y1) = nrect
        tx, rx = x // width, x % width
        ty, ry = y // height, y % height
        if x0 <= x < x1 and y0 <= y < y1:
            rx, ry = x, y
        else:
            if tx < 0:
                rx += x0
            elif tx > 0:
                rx += x1 - width
            if ty < 0:
                ry += y0
            elif ty > 0:
                ry += y1 - height

        d = ndistance.get((rx, ry), -1)
        if d < 0:
            return -1

        return d + abs(x-sx) + abs(y-sy)

    def count_diamond(steps):
        count = 0
        for y in range(-steps, steps+1):
            x0 = abs(y)-steps
            x1 = 1 - x0
            for x in range(x0, x1, 2):
                d = get_value(sx+x, sy+y)
                if 0 <= d <= steps:
                    count += 1

        return count

    def tile_count(tx, ty, steps, rem):
        x0 = tx * width
        x1 = x0 + width
        y0 = ty * height
        y1 = y0 + height
        count = 0
        for y in range(y0, y1):
            for x in range(x0, x1):
                d = get_value(x, y)
                if d < 0:
                    continue
                if d <= steps and d % 2 == rem:
                    count += 1
        return count

    # assert tile_count(-1, 0) == tile_count(-3, 0)
    # assert tile_count(-1, 0) != tile_count(-2, 0)
    # assert tile_count(-2, 0) == tile_count(-4, 0)

    def count_diamond_fast(steps):
        rem = steps % 2

        # center
        value = tile_count(0, 0, steps, rem)

        # arrows
        #      2
        #      |
        #      |
        #      |
        #      |
        # 1----S----3
        #      |
        #      |
        #      |
        #      |
        #      4
        count = (steps - sx + width - 1) // width
        if count > 0:
            value += tile_count(-count, 0, steps, rem)
            value += tile_count(0, -count, steps, rem)
            value += tile_count(count, 0, steps, rem)
            value += tile_count(0, count, steps, rem)
            if count - 1 > 0 and (steps + sx) % width <= width // 2:
                count -= 1
                value += tile_count(-count, 0, steps, rem)
                value += tile_count(0, -count, steps, rem)
                value += tile_count(count, 0, steps, rem)
                value += tile_count(0, count, steps, rem)

        # with borders
        #     1^2
        #    11|22
        #   11 | 22
        #  11  |  22
        # 11   |   22
        # <----S---->
        # 44   |   33
        #  44  |  33
        #   44 | 33
        #    44|33
        #      v
        # outer borders
        if count > 0:
            value += count * tile_count(-count, -1, steps, rem)
            value += count * tile_count(1, -count, steps, rem)
            value += count * tile_count(count, 1, steps, rem)
            value += count * tile_count(-1, count, steps, rem)

        # inner borders
        count -= 1
        if count > 0:
            value += count * tile_count(-count, -1, steps, rem)
            value += count * tile_count(1, -count, steps, rem)
            value += count * tile_count(count, 1, steps, rem)
            value += count * tile_count(-1, count, steps, rem)

        # with axes
        #      ^
        #      +
        #      *
        #      +
        #      *
        # <+*+*S*+*+>
        #      *
        #      +
        #      *
        #      +
        #      v
        if count > 0:
            even = count // 2
            odd = count - even
            value += odd * tile_count(-1, 0, steps, rem)
            value += odd * tile_count(0, -1, steps, rem)
            value += odd * tile_count(1, 0, steps, rem)
            value += odd * tile_count(0, 1, steps, rem)
            value += even * tile_count(-1, 0, steps, 1-rem)
            value += even * tile_count(0, -1, steps, 1-rem)
            value += even * tile_count(1, 0, steps, 1-rem)
            value += even * tile_count(0, 1, steps, 1-rem)

        # steps per quadrant
        #      v
        #     /|\
        #    /*|*\
        #   /*+|+*\
        #  /*+*|*+*\
        # <----S---->
        #  \*+*|*+*/
        #   \*+|+*/
        #    \*|*/
        #     \|/
        #      v
        if count > 0:
            even, odd = 0, 0
            for i in range(1, count):
                even, odd = odd + i, even

            if count % 2 == 1:
                even, odd = odd, even

            value += even * tile_count(-1, -1, steps, rem)
            value += even * tile_count(1, -1, steps, rem)
            value += even * tile_count(1, 1, steps, rem)
            value += even * tile_count(-1, 1, steps, rem)
            value += odd * tile_count(-1, -1, steps, 1-rem)
            value += odd * tile_count(1, -1, steps, 1-rem)
            value += odd * tile_count(1, 1, steps, 1-rem)
            value += odd * tile_count(-1, 1, steps, 1-rem)

        return value

    print("Part1:", count_diamond(64))

    # assert count_diamond(6) == count_diamond_fast(6)
    # assert count_diamond(10) == count_diamond_fast(10)
    # assert count_diamond(50) == count_diamond_fast(50)
    # assert count_diamond(100) == count_diamond_fast(100)
    # assert count_diamond(500) == count_diamond_fast(500)
    # assert count_diamond(1000) == count_diamond_fast(1000)
    # assert count_diamond(5000) == count_diamond_fast(5000)

    print("Part2:", count_diamond_fast(26501365))
