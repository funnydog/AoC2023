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

    def parse_workflow(line):
        lbrace = line.find("{")
        rbrace = line.rfind("}")
        if lbrace < 0 or rbrace < 0:
            raise RuntimeError("Cannot parse the line")

        name = line[0:lbrace]
        rules = []
        for rule in line[lbrace+1:rbrace].split(","):
            semicolon = rule.find(":")
            if semicolon < 0:
                # NOTE: dummy rule that's always true
                rules.append(("x", ">", -1, rule))
            else:
                rules.append((rule[0], rule[1], int(rule[2:semicolon]), rule[semicolon+1:]))

        return name, rules

    def parse_ratings(part):
        x, m, a, s = 0, 0, 0, 0
        for rating in part[1:-1].split(","):
            name, value = rating.split("=")
            if name == "x":
                x = int(value)
            elif name == "m":
                m = int(value)
            elif name == "a":
                a = int(value)
            elif name == "s":
                s = int(value)
        return x, m, a, s

    def execute(x, m, a, s):
        global workflows
        cur = "in"
        while cur != "A" and cur != "R":
            rules = workflows[cur]
            for name, op, number, target in rules:
                if name == "x":
                    value = x
                elif name == "m":
                    value = m
                elif name == "a":
                    value = a
                elif name == "s":
                    value = s
                if op == ">" and value > number:
                    cur = target
                    break
                if op == "<" and value < number:
                    cur = target
                    break
        return cur

    points = 0
    workflows = {}
    WORKFLOWS, RATINGS = 0, 1
    state = WORKFLOWS
    for line in lines:
        if state == WORKFLOWS:
            if line:
                name, rules = parse_workflow(line)
                workflows[name] = rules
            else:
                state = RATINGS
        elif state == RATINGS:
            x, m, a, s = parse_ratings(line)
            if execute(x, m, a, s) == "A":
                points += x + m + a + s
        else:
            raise RuntimeError("unknown state")

    print("Part1:", points)

    EMPTY = (-1, 0)

    def split(interval, op, number):
        global empty

        low, high = interval
        if high < number:
            if op == "<":
                return interval, EMPTY
            if op == ">":
                return EMPTY, interval
        elif number < low:
            if op == "<":
                return EMPTY, interval
            if op == ">":
                return interval, EMPTY
        elif op == "<":
            return (low, number-1), (number, high)
        elif op == ">":
            return (number+1, high), (low, number)

        raise RuntimeError("Unknown op {}".format(op))

    def combs(target, x, m, a, s):
        if target == "R":
            return 0

        if target == "A":
            return (x[1]-x[0]+1)*(m[1]-m[0]+1)*(a[1]-a[0]+1)*(s[1]-s[0]+1)

        value = 0
        for name, op, number, next_target in workflows[target]:
            if name == "x":
                xx, x = split(x, op, number)
                value += combs(next_target, xx, m, a, s)
            elif name == "m":
                mm, m = split(m, op, number)
                value += combs(next_target, x, mm, a, s)
            elif name == "a":
                aa, a = split(a, op, number)
                value += combs(next_target, x, m, aa, s)
            elif name == "s":
                ss, s = split(s, op, number)
                value += combs(next_target, x, m, a, ss)
        return value

    print("Part2:", combs("in", (1, 4000), (1, 4000), (1, 4000), (1, 4000)))
