#!/usr/bin/env python3
from typing import Any

import sys

FLIP_FLOP, CONJUNCTION, OTHER = 0, 1, 2

class Module(object):
    def __init__(self, name: str, typ: int, adj: list[str]) -> None:
        self.name = name
        self.typ = typ
        self.adj = adj
        self.flipflop = False
        self.conj: dict[str, int] = {}

LOW, HIGH = 0, 1

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

    LOW, HIGH = 0, 1

    modules: dict[str, Module] = {}
    inputs: dict[str, list[str]] = {}
    for line in lines:
        name, adj = line.split(" -> ")
        adjacents = adj.split(", ")
        if name.startswith("%"):
            typ = FLIP_FLOP
            name = name[1:]
        elif name.startswith("&"):
            typ = CONJUNCTION
            name = name[1:]
        else:
            typ = OTHER
        modules[name] = Module(name, typ, adjacents)
        for a in adjacents:
            inputs.setdefault(a, []).append(name)

    def simulate(start: str) -> tuple[int, int]:
        lows, highs = 0, 0
        queue = []
        queue.append(("button", start, LOW, 0))
        while queue:
            src, dst, pulse, count = queue.pop(0)

            # call the passed function for each event
            if pulse == LOW:
                lows += 1
            else:
                highs += 1

            m = modules.get(dst)
            if not m:
                continue
            elif m.typ == FLIP_FLOP:
                if pulse == HIGH:
                    pass
                else:
                    m.flipflop = not m.flipflop
                    if m.flipflop:
                        pulse = HIGH
                    else:
                        pulse = LOW
                    src = dst
                    for dst in m.adj:
                        queue.append((src, dst, pulse, count+1))
            elif m.typ == CONJUNCTION:
                m.conj[src] = pulse
                if (all(m.conj.get(src, LOW) == HIGH for src in inputs[dst])):
                    pulse = LOW
                else:
                    pulse = HIGH
                src = dst
                for dst in m.adj:
                    queue.append((src, dst, pulse, count+1))
            elif m.typ == OTHER:
                src = dst
                for dst in m.adj:
                    queue.append((src, dst, pulse, count+1))
            else:
                raise RuntimeError("Unknown module type")

        return lows, highs

    lows, highs = 0, 0
    for i in range(1000):
        l, h = simulate("broadcaster")
        lows += l
        highs += h

    print("Part1:", lows * highs)

    # reset the circuit
    for m in modules.values():
        m.flipflop = False
        m.conj = {}

    # get the period of each node connected to "broadcaster" and
    # multiply them
    value = 1
    for name in modules["broadcaster"].adj:
        # compute the period
        i = 0
        while True:
            simulate(name)
            i += 1

            # check if all the flip-flops are off
            for m in modules.values():
                if m.flipflop:
                    break
            else:
                break
        value *= i

    print("Part2:", value)
