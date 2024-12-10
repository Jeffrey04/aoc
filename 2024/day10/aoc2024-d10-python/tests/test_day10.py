from aoc2024_d10_python.day10 import (
    climb,
    find_trailheads,
    next_step,
    parse,
    part1,
    part2,
)


def test_parse() -> None:
    input = """
0123
1234
8765
9876
"""
    expected = {
        (0, 0): 0,
        (1, 0): 1,
        (2, 0): 2,
        (3, 0): 3,
        (0, 1): 1,
        (1, 1): 2,
        (2, 1): 3,
        (3, 1): 4,
        (0, 2): 8,
        (1, 2): 7,
        (2, 2): 6,
        (3, 2): 5,
        (0, 3): 9,
        (1, 3): 8,
        (2, 3): 7,
        (3, 3): 6,
    }

    assert parse(input) == expected


def test_next_step() -> None:
    topo_map = {
        (0, 0): 0,
        (1, 0): 1,
        (2, 0): 2,
        (3, 0): 3,
        (0, 1): 1,
        (1, 1): 2,
        (2, 1): 3,
        (3, 1): 4,
        (0, 2): 8,
        (1, 2): 7,
        (2, 2): 6,
        (3, 2): 5,
        (0, 3): 9,
        (1, 3): 8,
        (2, 3): 7,
        (3, 3): 6,
    }
    input1 = (0, 0)

    expected = ((1, 0), (0, 1))

    assert (input2 := next_step(topo_map, *input1)) == expected

    expected = ((2, 0), (1, 1))

    assert (input3 := next_step(topo_map, *input2[0])) == expected

    expected = ((3, 0), (2, 1))

    assert (input4 := next_step(topo_map, *input3[0])) == expected

    expected = ((3, 1),)

    assert (input5 := next_step(topo_map, *input4[0])) == expected

    expected = ((3, 2),)

    assert (input6 := next_step(topo_map, *input5[0])) == expected

    expected = ((3, 3), (2, 2))

    assert (input7 := next_step(topo_map, *input6[0])) == expected

    expected = ((2, 3),)

    assert (input8 := next_step(topo_map, *input7[0])) == expected

    expected = ((1, 3),)

    assert (input9 := next_step(topo_map, *input8[0])) == expected

    expected = ((0, 3),)

    assert (next_step(topo_map, *input9[0])) == expected


def test_find_trailheads() -> None:
    input = {
        (0, 0): 0,
        (1, 0): 1,
        (2, 0): 2,
        (3, 0): 3,
        (0, 1): 1,
        (1, 1): 2,
        (2, 1): 3,
        (3, 1): 4,
        (0, 2): 8,
        (1, 2): 7,
        (2, 2): 6,
        (3, 2): 5,
        (0, 3): 9,
        (1, 3): 8,
        (2, 3): 7,
        (3, 3): 6,
    }
    expected = ((0, 0),)

    assert find_trailheads(input) == expected


def test_climb() -> None:
    topo_map = parse("""
...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9
""")
    expected = 2

    assert len(climb(topo_map, find_trailheads(topo_map))) == expected

    topo_map = parse("""
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
""")
    expected = 4

    assert len(climb(topo_map, find_trailheads(topo_map))) == expected

    topo_map = parse("""
10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01
""")
    expected = 2 + 1

    assert len(climb(topo_map, find_trailheads(topo_map))) == expected

    topo_map = parse("""
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
""")
    expected = 36

    assert len(climb(topo_map, find_trailheads(topo_map))) == expected


def test_part1() -> None:
    input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    expected = 36

    assert part1(input) == expected


def test_part2() -> None:
    input = """
.....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....
"""
    expected = 3

    assert part2(input) == expected

    input = """
..90..9
...1.98
...2..7
6543456
765.987
876....
987....
"""
    expected = 13

    assert part2(input) == expected

    input = """
012345
123456
234567
345678
4.6789
56789.
"""
    expected = 227

    assert part2(input) == expected

    input = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""
    expected = 81

    assert part2(input) == expected
