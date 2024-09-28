#!/usr/bin/env python3
import random
import sys

class Karger(object):
    def __init__(self) -> None:
        self.rank: dict[str, int] = {}
        self.parent: dict[str, str] = {}

    def find(self, node: str) -> str:
        parent = self.parent.get(node, node)
        if parent != node:
            parent = self.parent[node] = self.find(parent)
        return parent

    def union(self, a: str, b: str) -> None:
        pa = self.find(a)
        pb = self.find(b)

        if pa == pb:
            return

        ra = self.rank.get(pa, 0)
        rb = self.rank.get(pb, 0)
        if ra < rb:
            self.parent[pa] = pb
        elif ra > rb:
            self.parent[pb] = pa
        else:
            self.parent[pb] = pa
            self.rank[pa] = rb + 1

    def mincut(self, vcount: int, edges: list[tuple[str, str]]) -> list[tuple[str, str]]:
        self.rank.clear()
        self.parent.clear()
        while vcount > 2:
            i = random.randint(0, len(edges)-1)
            u, w = map(self.find, edges.pop(i))
            if u != w:
                vcount -= 1
                self.union(u, w)

        return [(u, w) for u, w in edges if self.find(u) != self.find(w)]

    def components(self, vertices: set[str]) -> list[list[str]]:
        comp: dict[str, list[str]] = {}
        for k in vertices:
            parent = self.find(k)
            comp.setdefault(parent, []).append(k)

        return list(comp.values())

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

    # Construct the graph
    edges: list[tuple[str, str]] = []
    vertices: set[str] = set()
    for line in lines:
        semi = line.find(":")
        if semi >= 0:
            src = line[:semi]
            vertices.add(src)
            for dst in line[semi+1:].split():
                vertices.add(dst)
                edges.append((src, dst))

    ka = Karger()
    while True:
        cuts = ka.mincut(len(vertices), edges.copy())
        if len(cuts) == 3:
            for c in cuts:
                edges.remove(c)
            break

    result = 1
    for lst in ka.components(vertices):
        result *= len(lst)

    print("Part1:", result)
