#!/usr/bin/env python3
from typing import Callable

import math
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = [x.strip() for x in f.readlines()]
    except:
        print(f"cannot open { sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    directions = lines[0].strip()
    mymap: dict[str, tuple[str, str]] = {}
    for line in lines[2:]:
        here, destinations = line.split("=")
        left, right = tuple(x.strip() for x in destinations.strip()[1:-1].split(","))
        mymap[here.strip()] = (left, right)

    def cycle(start: str, endp: Callable[[str], bool]) -> int:
        if start not in mymap:
            return 0
        count, i = 0, 0
        while not endp(start):
            idx = directions[i] == "R" and 1 or 0
            i += 1
            if i >= len(directions):
                i = 0
            start = mymap[start][idx]
            count += 1
        return count

    print("Part1:", cycle("AAA", lambda x: x == "ZZZ"))

    values: list[int] = []
    for x in mymap.keys():
        if x.endswith("A"):
            values.append(cycle(x, lambda x: x.endswith("Z")))

    print("Part2:", math.lcm(*values))
