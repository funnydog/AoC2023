#!/usr/bin/env python3
from functools import cmp_to_key
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

    def get_type(hand: str, cards: str) -> int:
        # count the cards in the hand
        count = [0] * len(cards)
        for card in hand:
            count[cards.index(card)] += 1

        # handle the Jolly special case
        jolly = 0
        if cards[-1] == "J":
            jolly = count[-1]
            count[-1] = 0

        count.sort(key = lambda x: -x)
        if count[0] + jolly >= 5:
            return 6            # five of a kind
        elif count[0] + jolly >= 4:
            return 5            # four of a kind
        elif count[0] + jolly >= 3 and count[1] == 2 or count[0] == 3 and count[1] + jolly >= 2:
            return 4            # full house
        elif count[0] + jolly >= 3:
            return 3            # tree of a kind
        elif count[0] + jolly >= 2 and count[1] == 2 or count[0] >= 2 and count[1] + jolly >= 2:
            return 2            # two pairs
        elif count[0] +jolly >= 2:
            return 1            # one pair
        else:
            return 0            # high card

    def card_cmp(a: str, b: str, cards: str) -> int:
        ta = get_type(a, cards)
        tb = get_type(b, cards)
        if ta != tb:
            return ta - tb

        pa = tuple(cards.index(c) for c in a)
        pb = tuple(cards.index(c) for c in b)
        if pa < pb:
            return 1
        elif pa > pb:
            return -1
        else:
            return 0

    cards1 = "AKQJT98765432"
    cards2 = "AKQT98765432J"

    assert get_type("23456", cards1) == 0
    assert get_type("233TK", cards1) == 1
    assert get_type("2233T", cards1) == 2
    assert get_type("22234", cards1) == 3
    assert get_type("22233", cards1) == 4
    assert get_type("22223", cards1) == 5
    assert get_type("22222", cards1) == 6

    assert get_type("T55J5", cards2) == 5
    assert get_type("KTJJT", cards2) == 5
    assert get_type("QQQJA", cards2) == 5

    assert card_cmp("KK677", "KTJJT", cards1) > 0
    assert card_cmp("T55J5", "QQQJA", cards1) < 0

    # parse the hands
    hands = []
    for line in lines:
        values = line.strip().split()
        hands.append((values[0],int(values[1])))

    part1 = 0
    hands.sort(key = lambda x: cmp_to_key(lambda a, b: card_cmp(a, b, cards1))(x[0]))
    for rank, hand in enumerate(hands, 1):
        part1 += rank * hand[1]

    part2 = 0
    hands.sort(key = lambda x: cmp_to_key(lambda a, b: card_cmp(a, b, cards2))(x[0]))
    for rank, hand in enumerate(hands, 1):
        part2 += rank * hand[1]

    print("Part1:", part1)
    print("Part2:", part2)
