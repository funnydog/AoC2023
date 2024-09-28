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

    bricks = []
    for line in lines:
        s0, s1 = line.split("~")
        p0 = tuple(int(x) for x in s0.split(","))
        p1 = tuple(int(x) for x in s1.split(","))
        assert p0[2] <= p1[2]
        bricks.append((p0, p1))

    def add(a, b):
        return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

    def scalar(a, s):
        return (a[0]*s, a[1]*s, a[2]*s)

    def translate(brick, v):
        return add(brick[0], v), add(brick[1], v)

    def intersect(a, b):
        for i in range(3):
            if a[1][i] < b[0][i] or a[0][i] > b[1][i]:
                return False
        return True

    assert intersect( ((1,0,1), (1,2,1)), ((1,0,1), (1,2,1)) )
    assert intersect( ((1,0,1), (1,2,1)), ((0,0,1), (2,0,1)) )

    # Make the bricks fall
    # sort the bricks by base z value
    bricks.sort(key = lambda x: x[0][2])
    floor: dict[tuple[int,int], int] = {}
    for i, brick in enumerate(bricks):
        maxf = 0
        for y in range(brick[0][1], brick[1][1]+1):
            for x in range(brick[0][0], brick[1][0]+1):
                v = floor.get((x, y), 0)
                if maxf < v:
                    maxf = v

        bricks[i] = translate(brick, scalar((0, 0, -1), (brick[0][2] - maxf - 1)))

        for y in range(brick[0][1], brick[1][1]+1):
            for x in range(brick[0][0], brick[1][0]+1):
                floor[x, y] = bricks[i][1][2]

    # # graph with bricks as nodes and the bricks staying on them as
    # # edges. The degree is the number of bricks supporting the current
    # # one.
    class Node(object):
        def __init__(self, brick):
            self.brick = brick
            self.degree = 0
            self.adj = []
            self.safe = False

    graph: list[Node] = []
    for i, brick in enumerate(bricks):
        but = translate(brick, (0, 0, -1))
        n = Node(brick)
        graph.append(n)
        for j in range(i):
            if intersect(but, bricks[j]):
                n.degree += 1
                graph[j].adj.append(i)

    # assume there is a fake node -1 representing the floor
    # and adjust the degree accordingly
    for node in graph:
        if node.degree == 0:
            node.degree = 1

    count = 0
    for i, node in enumerate(graph):
        if all(graph[j].degree > 1 for j in node.adj):
            node.safe = True
            count += 1

    print("Part1:", count)

    def destroy(graph, k):
        degrees = [node.degree for node in graph]
        queue = [k]
        while queue:
            i = queue.pop()
            for j in graph[i].adj:
                degrees[j] -= 1
                if degrees[j] == 0:
                    queue.append(j)

        count = 0
        for j in range(k+1, len(graph)):
            if degrees[j] == 0:
                count += 1

        return count

    count = 0
    for i, node in enumerate(graph):
        count += destroy(graph, i)

    print("Part2:", count)
