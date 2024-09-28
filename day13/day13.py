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

    def vertical_reflections(m):
        height, width = len(m), len(m[0])
        ref = 0
        for x in range(1, width):
            mirror = True
            for i in range(x):
                x1 = x + i
                if x1 >= width:
                    break
                x2 = x - i - 1
                for y in range(height):
                    if m[y][x1] != m[y][x2]:
                        mirror = False
                        break
            if mirror:
                ref |= 1 << (x-1)
        return ref

    def horizontal_reflections(m):
        height, width = len(m), len(m[0])
        ref = 0
        for y in range(1, height):
            mirror = True
            for i in range(y):
                y1 = y + i
                if y1 >= height:
                    break
                y2 = y - i - 1
                if m[y1] != m[y2]:
                    mirror = False
                    break
            if mirror:
                ref |= 1 << (y-1)
        return ref

    def get_reflections(m):
        return horizontal_reflections(m) << 32 | vertical_reflections(m)

    def log2(x):
        i = 0
        while x:
            x >>= 1
            i += 1
        return i

    def get_points(ref):
        return log2(ref>>32) * 100 + log2(ref&0xFFFFFFFF)

    def fixed_mirror(m, oldref):
        height, width = len(m), len(m[0])
        for y in range(height):
            for x in range(width):
                m[y][x] = m[y][x] == "." and "#" or "."
                newref = get_reflections(m) & ~oldref
                m[y][x] = m[y][x] == "." and "#" or "."
                if newref:
                    return newref
        return 0

    part1, part2 = 0, 0
    m = []
    lines.append("")
    for line in lines:
        if line:
            m.append(list(line))
        else:
            reflections = get_reflections(m)
            part1 += get_points(reflections)
            part2 += get_points(fixed_mirror(m, reflections))
            m = []

    print("Part1:", part1)
    print("Part2:", part2)
