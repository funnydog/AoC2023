#!/usr/bin/env python3
from fractions import Fraction
from functools import reduce

import sys
import math

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


    lst = []
    for line in lines:
        a, b = line.split(" @ ")
        lst.append((
            tuple(int(x) for x in a.split(", ")),
            tuple(int(x) for x in b.split(", "))
        ))

    def add(a, b):
        return (a[0]+b[0], a[1]+b[1], a[2]+b[2])

    def sub(a, b):
        return (a[0]-b[0], a[1]-b[1], a[2]-b[2])

    def scale(a, b):
        return (a[0]*b, a[1]*b, a[2]*b)

    def cross(a, b):
        return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

    def dot(a, b):
        return a[0]*b[0] + a[1]*b[1] + a[2]*b[2]

    def norm(a):
        f = 1.0 / math.sqrt(a[0]*a[0] + a[1]*a[1] + a[2]*a[2])
        return scale(a, f)

    def intersect_xy(la, lb):
        x1, y1, _ = la[0]
        x2, y2, _ = add(la[0], scale(la[1], max(la[0])/max(la[1])))
        x3, y3, _ = lb[0]
        x4, y4, _ = add(lb[0], scale(lb[1], max(lb[0])/max(lb[1])))

        den = (x1-x2)*(y3-y4) - (y1-y2)*(x3-x4)
        if den == 0:
            return None

        i = (x1*y2-y1*x2)
        j = (x3*y4-y3*x4)
        return (
            (i*(x3-x4) - (x1-x2)*j) / den,
            (i*(y3-y4) - (y1-y2)*j) / den
        )

    count = 0
    if sys.argv[1] == "test":
        minv, maxv = 7, 27
    else:
        minv, maxv = 200000000000000, 400000000000000
    for i, la in enumerate(lst):
        for j in range(i):
            lb = lst[j]
            p = intersect_xy(la, lb)
            if p:
                time_a = (p[0]-la[0][0]) / (la[1][0])
                time_b = (p[0]-lb[0][0]) / (lb[1][0])
                # print(i, j, time_a, time_b)
                if minv <= p[0] <= maxv and minv <= p[1] <= maxv:
                    if time_a >= 0 and time_b >= 0:
                        count += 1

    print("Part1:", count)

    p0, d0 = lst[0]
    p1, d1 = lst[1]
    p2, d2 = lst[2]

    p1 = sub(p1, p0)
    d1 = sub(d1, d0)

    p2 = sub(p2, p0)
    d2 = sub(d2, d0)

    # the collision with p0 is always at 0
    # the other two collision are at p1+t1*d1 and p2+t2*d2
    # The tree collision are collinear so the cross product is zero:
    #
    # (p1 + t1 * d1) x (p2 + t2 * d2) = 0
    #
    # (p1 x p2) + t1 * (d1 x p2) + t2 * (p1 x d2) + t1*t2*(d1 x d2) = 0
    #
    # Interaction cross and dot product
    # (a x b) * a = (a x b) * b = 0
    #
    # dot product with d2
    # (p1 x p2) * d2 + t1 * (d1 x p2) * d2 = 0
    #
    # t1 = -((p1 x p2) * v2)/((d1 x p2) * d2)
    #
    # dot product with d1
    #
    # (p1 x p2) * d1 + t2 * (p1 x d2) * d1 = 0
    #
    # t2 = -((p1 x p2) * d1)/((p1 x d2) * d1)

    t1 = -dot(cross(p1, p2), d2) / dot(cross(d1, p2), d2)
    t2 = -dot(cross(p1, p2), d1) / dot(cross(p1, d2), d1)

    # find the actual point of intersection given t1 and t2
    p1, d1 = lst[1]
    p2, d2 = lst[2]
    c1 = add(p1, scale(d1, t1))
    c2 = add(p2, scale(d2, t2))

    # find the velocity as (c2-c1) / (t2-t1)
    v = scale(sub(c2, c1), 1/(t2-t1))

    # find the position using the velocity and a point of intersection
    p = sub(c1, scale(v, t1))

    print("Part2:", int(sum(p)))
