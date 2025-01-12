from itertools import permutations

from aoc2024_d23_python.day23 import (
    network_find_parties,
    parse,
    part1,
    part2,
    parties_filter_chief,
)

input = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""


def test_network_find_connected_nodes() -> None:
    network = parse(input)
    expected = """
aq,cg,yn
aq,vc,wq
co,de,ka
co,de,ta
co,ka,ta
de,ka,ta
kh,qp,ub
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
ub,vc,wq
""".strip().splitlines()

    result = tuple(network_find_parties(network, 3))
    assert len(expected) == len(result)

    for nodes in result:
        assert any(
            ",".join(map(lambda x: x.name, combo)) in expected
            for combo in permutations(nodes, 3)
        )


def test_party_find_t() -> None:
    network = parse(input)
    expected = """
co,de,ta
co,ka,ta
de,ka,ta
qp,td,wh
tb,vc,wq
tc,td,wh
td,wh,yn
""".strip().splitlines()

    result = tuple(parties_filter_chief(network_find_parties(network, 3)))
    assert len(expected) == len(result)

    for nodes in result:
        assert any(
            ",".join(map(lambda x: x.name, combo)) in expected
            for combo in permutations(nodes, 3)
        )


def test_part1() -> None:
    expected = 7

    assert part1(input) == expected


def test_part2() -> None:
    expected = "co,de,ka,ta"

    assert part2(input) == expected
