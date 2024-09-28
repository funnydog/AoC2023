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

    def hashfn(s: str) -> int:
        value = 0
        for c in s:
            value += ord(c)
            value *= 17
            value &= 255
        return value

    assert hashfn("HASH") == 52

    count = 0
    for line in lines:
        for step in line.split(","):
            count += hashfn(step)

    print("Part1:", count)

    boxes: list[list[tuple[str, int]]] = [[] for i in range(256)]
    for line in lines:
        for step in line.split(","):
            pos = step.find("-")
            if pos < 0:
                pos = step.find("=")

            label = step[:pos]
            op = step[pos]
            arg = step[pos+1:]

            box = boxes[hashfn(label)]
            idx = -1
            for i, (l, fl) in enumerate(box):
                if label == l:
                    idx = i
                    break

            if op == "-":
                if idx >= 0:
                    box.pop(i)
            elif op == "=":
                if idx >= 0:
                    box[idx] = (label, int(arg))
                else:
                    box.append((label, int(arg)))

    total_power = 0
    for power, box in enumerate(boxes, 1):
        for slot, (label, focal_length) in enumerate(box, 1):
            total_power += power * slot * focal_length

    print("Part2:", total_power)
