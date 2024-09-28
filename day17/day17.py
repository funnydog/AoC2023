#!/usr/bin/env python3
from heapq import heappush, heappop

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
    m = [[int(x) for x in row] for row in lines]

    NORTH, WEST, SOUTH, EAST = 0, 1, 2, 3
    dirname = ["NORTH", "WEST", "SOUTH", "EAST"]


    def solve(start, d, minsteps, maxsteps):
        d = EAST
        heat = {start: 0}
        parent = {start: start}
        visited = {(start[0],start[1], -1, 0): True}
        queue = []
        queue.append((0, 0, 1, -1, start))
        while queue:
            eh, h, l, d, (x, y) = heappop(queue)
            if x == width -1 and y == height -1 and l >= minsteps:
                return h

            for nd in (NORTH, WEST, SOUTH, EAST):
                if (nd + 2) % 4 == d: # don't go back
                    continue
                elif d != -1 and d != nd and l < minsteps: # min steps constraint
                    continue
                elif d != nd:   # change of direction
                    nl = 1
                elif l < maxsteps: # same direction
                    nl = l + 1
                else:           #  not allowed
                    continue

                if nd == NORTH:
                    nx, ny = x, y-1
                elif nd == WEST:
                    nx, ny = x-1, y
                elif nd == SOUTH:
                    nx, ny = x, y+1
                elif nd == EAST:
                    nx, ny = x+1, y
                if nx < 0 or nx >= width or ny < 0 or ny >= height:
                    continue

                nh = h + m[ny][nx]
                if (nx, ny, nd, nl) in visited:
                    continue

                visited[nx, ny, nd, nl] = True
                eh = nh + width + height - nx - ny - 2

                heappush(queue, (eh, nh, nl, nd, (nx, ny)))

        exit(1)

    print("Part1:", solve((0,0), EAST, 1, 3))
    print("Part2:", solve((0,0), EAST, 4, 10))
