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

    def listfind(lst, value, start):
        try:
            lst.index(value, start)
            return True
        except ValueError:
            return False

    cache = {}
    def cw(record, start, rules):
        global cache
        # Reset the cache if we start from zero
        if start == 0:
            cache = {}

        # Get the result from the cache if already computed
        args = (record, start, tuple(rules))
        if args in cache:
            return cache[args]

        # compute the value
        retvalue = 0
        if not rules and listfind(record, "#", start):
            pass
        elif not rules:
            retvalue = 1
        elif start >= len(record):
            pass
        else:
            # find the interval of interest where we could place the string
            while start < len(record) and record[start] == ".":
                start += 1
            end = start
            while end < len(record) and record[end] in "?#":
                end += 1

            # try to fit the string inside the interval
            rule = rules[0]
            for i in range(start, end - rule + 1):
                # print("{}{}".format("*" * start, record[start:]), start, end, rule)
                if i > 0 and record[i-1] == '#':
                    # NOTE: this would enlarge the string also don't
                    # proceed further because we have a fixed dash
                    break
                elif i + rule < len(record) and record[i + rule] == '#':
                    # NOTE: this would enlarge the string but we can
                    # proceed further
                    pass
                else:
                    # NOTE: compute the count for the next rules from
                    # the end of the string + 1
                    retvalue += cw(record, i+rule+1, rules[1:])
            if not "#" in record[start:end]:
                # NOTE: if there isn't any dash inside the interval we
                # can skip it altogether
                retvalue += cw(record, end, rules)

        cache[args] = retvalue
        return retvalue

    assert cw("?##", 0, [3]) == 1
    assert cw("???.###", 0, [1,1,3]) == 1
    assert cw(".??..??...?##.", 0, [1,1,3]) == 4
    assert cw("?#?#?#?#?#?#?#?", 0, [1,3,1,6]) == 1
    assert cw("????.#...#...", 0, [4,1,1]) == 1
    assert cw("????.######..#####.", 0, [1,6,5]) == 4
    assert cw("?###????????", 0, [3,2,1]) == 10
    assert cw("?????.?#????", 0, [1, 2, 1, 1]) == 14
    assert cw("??#?#?.#??.?", 0, [1, 1, 1, 1]) == 3

    count = 0
    for line in lines:
        record, rules = line.split()
        rules = [int(x) for x in rules.split(",")]
        a = cw(record, 0, rules)
        #b = count_ways(record, rules)
        #print (record, rules, a, b)
        #assert a == b
        count += a

    print("Part1:", count)

    count = 0
    for line in lines:
        record, rules = line.split()
        count += cw("?".join([record]*5), 0, [int(x) for x in rules.split(",")]*5)
    print("Part2:", count)
