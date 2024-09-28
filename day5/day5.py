#!/usr/bin/env python3
import sys

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

    # naive parsing
    def range_to_interval(line: str) -> (int, int, int):
        dst, src, length = tuple(int(x) for x in line.split())
        return src, src + length, dst - src

    def apply_map(a, mymap):
        newset = []
        i = 0
        while i < len(mymap):
            b = mymap[i]
            if a[1] <= b[0]:    # do not overlap
                break
            elif b[1] <= a[0]:  # do not overlap
                i += 1
            elif a[0] < b[0]:
                newset.append((a[0], b[0], 0))
                a = (b[0], a[1], 0)
            elif a[1] > b[1]:
                newset.append((a[0]+b[2], b[1]+b[2], 0))
                a = (b[1], a[1], 0)
                i += 1
            else:
                newset.append((a[0]+b[2], a[1]+b[2], 0))
                return newset

        newset.append(a)
        return newset

    def transform(seeds, mymap):
        newseeds = []
        for s in seeds:
            newseeds.extend(apply_map(s, mymap))
        newseeds = [x for x in newseeds if x[0] != x[1]]
        return sorted(newseeds, key=lambda x: x[0])

    part1: list[(int,int,int)] = []
    part2: list[(int,int,int)] = []
    mymap: list[(int,int,int)] = []
    lines.append("\n")
    for line in lines:
        line = line.strip()
        if not line:
            if mymap:
                mymap.sort(key = lambda x: x[0])
                part1 = transform(part1, mymap)
                part2 = transform(part2, mymap)
        elif line.startswith("seeds:"):
            numbers = [int(x) for x in line.split(":")[1].strip().split()]
            part1 = sorted(
                [(x, x+1, 0) for x in numbers],
                key=lambda x: x[0]
            )
            part2 = sorted(
                [(numbers[i], numbers[i] + numbers[i+1], 0) for i in range(0, len(numbers), 2)],
                key=lambda x: x[0]
            )
        elif ":" in line:
            mymap = []
        else:
            mymap.append(range_to_interval(line))

    print("Part1:", part1[0][0])
    print("Part2:", part2[0][0])
