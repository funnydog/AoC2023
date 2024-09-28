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

    sumfirst, sumlast = 0, 0
    for line in lines:
        seq = [int(x) for x in line.split()]
        i = 0
        while not all(x == 0 for x in seq):
            if (i % 2) == 0:
                sumfirst += seq[0]
            else:
                sumfirst -= seq[0]
            i += 1
            sumlast += seq[-1]
            seq = [(b - a) for a, b in zip(seq, seq[1:])]

    print("Part1:", sumlast)
    print("Part2:", sumfirst)
