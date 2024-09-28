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

    height, width = len(lines), len(lines[0])
    start = (1, 0)
    end = (width-2, height-1)

    class Node(object):
        def __init__(self, slope, pos):
            self.slope = slope
            self.pos = pos
            self.visited = False
            self.distance = 0
            self.adj = []
            self.incoming = []

    # create the graph of slopes
    graph = []
    slopes = {start: 0}
    graph.append(Node(".", start))
    for y in range(height):
        for x in range(width):
            if lines[y][x] in "<^>v":
                slopes[x, y] = len(graph)
                graph.append(Node(lines[y][x], (x, y)))

    slopes[end] = len(graph)
    graph.append(Node(".", end))

    # add the edges
    def add_edges(graph, slopes, wet=True):
        neighbors = [(-1, 0), (0, -1), (1, 0), (0, 1)]
        for i, n in enumerate(graph):
            n.adj = []
            s, pos = 0, n.pos
            distance = {pos: s}
            k = "<^>v".find(lines[pos[1]][pos[0]])
            if wet and k >= 0:
                pos = (pos[0]+neighbors[k][0], pos[1]+neighbors[k][1])
                s += 1
                distance[pos] = s
            queue = [(s, pos)]
            while queue:
                s, (x, y) = queue.pop(0)
                k = "<^>v".find(lines[y][x])
                if not wet or k < 0:
                    candidates = neighbors
                else:
                    candidates = neighbors[k:k+1]
                candidates = neighbors
                for dx, dy in candidates:
                    ns, nx, ny = s+1, x+dx, y+dy
                    if nx < 0 or nx >= width or ny < 0 or ny >= height:
                        continue
                    elif (nx, ny) in distance:
                        continue
                    elif wet and dx > 0 and lines[ny][nx] == "<":
                        continue
                    elif wet and dx < 0 and lines[ny][nx] == ">":
                        continue
                    elif wet and dy > 0 and lines[ny][nx] == "^":
                        continue
                    elif wet and dy < 0 and lines[ny][nx] == "v":
                        continue
                    elif (nx, ny) in slopes:
                        distance[nx, ny] = ns
                        j = slopes[nx, ny]
                        graph[j].incoming.append((ns, i))
                        n.adj.append((ns, slopes[nx, ny]))
                    elif lines[ny][nx] == ".":
                        distance[nx, ny] = ns
                        queue.append((ns, (nx, ny)))

    def find_longest(graph):
        best = 0
        def backtrack(graph, pos, end, dist):
            nonlocal best
            if pos == end:
                if best < dist:
                    best = dist
            else:
                for w, i in graph[pos].adj:
                    if not graph[i].visited:
                        # if we take this path we have to mark all the
                        # other vertices of the graph as visited because
                        # we cannot walk on a path already taken
                        backup = []
                        for _, j in graph[pos].adj:
                            backup.append((j, graph[j].visited))
                            graph[j].visited = True
                        backtrack(graph, i, end, dist + w)
                        for j, val in backup:
                            graph[j].visited = val

        graph[0].visited = True
        backtrack(graph, 0, len(graph)-1, 0)
        return best

    # def bellman_ford(graph, s):
    #     # initialize the distance and predecessor
    #     distance = []
    #     predecessor = []
    #     for i, n in enumerate(graph):
    #         distance.append(10000000)
    #         predecessor.append(None)

    #     distance[s] = 0

    #     # relaxation
    #     for i in range(len(graph)-1):
    #         succeeded = False
    #         for j, n in enumerate(graph):
    #             for w, k in n.adj:
    #                 if distance[j]-w < distance[k]:
    #                     distance[k] = distance[j]-w
    #                     predecessor[k] = j
    #                     succededed = True

    #         if not succeeded:
    #             break

    #     return distance, predecessor

    # def topsort(graph):
    #     visited = set()
    #     v = []
    #     def dfs(graph, i):
    #         nonlocal visited, v
    #         if i in visited:
    #             return

    #         visited.add(i)
    #         for _, j in graph[i].adj:
    #             dfs(graph, j)

    #         v.append(i)

    #     for i in range(len(graph)):
    #         dfs(graph, i)

    #     v.reverse()
    #     return v

    # add_edges(graph, slopes, wet=True)
    # distance = [-1]*len(graph)
    # distance[0] = 0
    # for v in topsort(graph):
    #     if distance[v] >= 0:
    #         for w, j in graph[v].adj:
    #             if distance[j] < distance[v] + w:
    #                 distance[j] = distance[v] + w

    # print(distance[-1])

    # add_edges(graph, slopes, wet=False)
    # distance = [-1]*len(graph)
    # distance[0] = 0
    # for v in topsort(graph):
    #     if distance[v] >= 0:
    #         for w, j in graph[v].adj:
    #             if distance[j] < distance[v] + w:
    #                 distance[j] = distance[v] + w
    # print(distance[-1])

    add_edges(graph, slopes, wet=True)
    print("Part1:", find_longest(graph))

    add_edges(graph, slopes, wet=False)
    print("Part2:", find_longest(graph))
