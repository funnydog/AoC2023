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

    def add(a, b):
        return (a[0]+b[0], a[1]+b[1])

    def mul(a, b):
        return (a[0]*b, a[1]*b)

    def get_vertices(cmds):
        # NOTE: move the vertex to right and down depending of the
        # turn we are going to make.
        fix = {
            "RU": (0, 0),
            "UR": (0, 0),
            "RD": (1, 0),
            "DR": (1, 0),
            "LU": (0, 1),
            "UL": (0, 1),
            "DL": (1, 1),
            "LD": (1, 1),
        }
        p = (0, 0)
        vertices = []
        for (d1, q), (d2, _) in zip(cmds, cmds[1:] + cmds[0:1]):
            if d1 == "U":
                d = (0, -1)
            elif d1 == "D":
                d = (0, 1)
            elif d1 == "L":
                d = (-1, 0)
            elif d1 == "R":
                d = (1, 0)
            else:
                raise RuntimeError(f"Unknown direction {d}")

            t = mul(d, q)
            p = add(p, t)
            vertices.append(add(p, fix[d1+d2]))

        return vertices

    def trapezoid(vertices):
        area = 0
        for (x0, y0), (x1, y1) in zip(vertices, vertices[1:] + vertices[0:1]):
            ar = x1 - x0
            ar *= y0
            area += ar
        return abs(area)

    def parse1(lines):
        cmds = []
        for line in lines:
            ds, qs, _ = line.split()
            cmds.append((ds, int(qs)))
        return cmds

    def parse2(lines):
        cmds = []
        dirmap = { "0": "R", "1": "D", "2": "L", "3": "U" }
        for line in lines:
            _, _, color = line.split()
            cmds.append((dirmap[color[-2]],int(color[2:-2], 16)))
        return cmds

    print("Part1:", trapezoid(get_vertices(parse1(lines))))
    print("Part2:", trapezoid(get_vertices(parse2(lines))))
