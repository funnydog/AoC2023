#!/usr/bin/env python3
import sys
import math

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"Usage: { sys.argv[0] } <filename>", file=sys.stderr)
        sys.exit(1)

    try:
        with open(sys.argv[1], "rt") as f:
            lines = f.readlines()
    except:
        print(f"cannot open { sys.argv[1] }", file=sys.stderr)
        sys.exit(1)

    time = []
    distance = []
    for line in lines:
        line.strip()
        if not line:
            pass
        elif line.startswith("Time:"):
            time = [int(x) for x in line.split(":")[1].strip().split()]
        elif line.startswith("Distance:"):
            distance = [int(x) for x in line.split(":")[1].strip().split()]
        else:
            pass

    def calc(x, t):
        return x*(t -x)

    def solutions(t, d):
        s = math.sqrt(t*t - 4*d)
        high = math.floor((t + s) / 2)
        low = math.ceil((t - s) / 2)

        # do this to avoid messing with an arbitrary epsilon
        value = high - low + 1
        if calc(high, t) == d:
            value -= 1
        if calc(low, t) == d:
            value -= 1

        return value

    part1 = 1
    for i, t in enumerate(time):
        d = distance[i]
        part1 *= solutions(t, distance[i])

    print("Part1:", part1)
    t = int("".join(str(x) for x in time))
    d = int("".join(str(x) for x in distance))
    print("Part2:", solutions(t, d))
