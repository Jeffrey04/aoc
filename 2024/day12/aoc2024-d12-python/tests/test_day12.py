import pytest

from aoc2024_d12_python.day12 import (
    Plant,
    cluster_build,
    cluster_get_neighbours_diff,
    cluster_get_neighbours_same,
    parse,
    part1,
    part2,
)


def test_parse() -> None:
    input = """
AAAA
BBCD
BBCC
EEEC
"""
    expected = {
        (0, 0): Plant("A", (0, 0)),
        (1, 0): Plant("A", (1, 0)),
        (2, 0): Plant("A", (2, 0)),
        (3, 0): Plant("A", (3, 0)),
        (0, 1): Plant("B", (0, 1)),
        (1, 1): Plant("B", (1, 1)),
        (2, 1): Plant("C", (2, 1)),
        (3, 1): Plant("D", (3, 1)),
        (0, 2): Plant("B", (0, 2)),
        (1, 2): Plant("B", (1, 2)),
        (2, 2): Plant("C", (2, 2)),
        (3, 2): Plant("C", (3, 2)),
        (0, 3): Plant("E", (0, 3)),
        (1, 3): Plant("E", (1, 3)),
        (2, 3): Plant("E", (2, 3)),
        (3, 3): Plant("C", (3, 3)),
    }

    assert parse(input) == expected


def test_cluster_get_neighbours_same() -> None:
    garden = {
        (0, 0): Plant("A", (0, 0)),
        (1, 0): Plant("A", (1, 0)),
        (2, 0): Plant("A", (2, 0)),
        (3, 0): Plant("A", (3, 0)),
        (0, 1): Plant("B", (0, 1)),
        (1, 1): Plant("B", (1, 1)),
        (2, 1): Plant("C", (2, 1)),
        (3, 1): Plant("D", (3, 1)),
        (0, 2): Plant("B", (0, 2)),
        (1, 2): Plant("B", (1, 2)),
        (2, 2): Plant("C", (2, 2)),
        (3, 2): Plant("C", (3, 2)),
        (0, 3): Plant("E", (0, 3)),
        (1, 3): Plant("E", (1, 3)),
        (2, 3): Plant("E", (2, 3)),
        (3, 3): Plant("C", (3, 3)),
    }
    input = (garden[(0, 0)],)
    expected = ((garden[(0, 0)], garden[(1, 0)]),)

    print(cluster_get_neighbours_same(garden, input))
    print(expected)
    assert cluster_get_neighbours_same(garden, input) == expected

    input = (garden[(2, 2)], garden[(3, 2)])
    expected = (
        (garden[(2, 2)], garden[(2, 1)]),
        (garden[(3, 2)], garden[(3, 3)]),
    )

    assert cluster_get_neighbours_same(garden, input) == expected


def test_cluster_get_neighbours_diff() -> None:
    garden = {
        (0, 0): Plant("A", (0, 0)),
        (1, 0): Plant("A", (1, 0)),
        (2, 0): Plant("A", (2, 0)),
        (3, 0): Plant("A", (3, 0)),
        (0, 1): Plant("B", (0, 1)),
        (1, 1): Plant("B", (1, 1)),
        (2, 1): Plant("C", (2, 1)),
        (3, 1): Plant("D", (3, 1)),
        (0, 2): Plant("B", (0, 2)),
        (1, 2): Plant("B", (1, 2)),
        (2, 2): Plant("C", (2, 2)),
        (3, 2): Plant("C", (3, 2)),
        (0, 3): Plant("E", (0, 3)),
        (1, 3): Plant("E", (1, 3)),
        (2, 3): Plant("E", (2, 3)),
        (3, 3): Plant("C", (3, 3)),
    }
    input = (garden[(0, 0)],)
    expected = (
        (garden[(0, 0)], None),
        (garden[(0, 0)], garden[(0, 1)]),
        (garden[(0, 0)], None),
    )

    print(cluster_get_neighbours_diff(garden, input))
    assert cluster_get_neighbours_diff(garden, input) == expected


def test_cluster_build() -> None:
    garden = {
        (0, 0): Plant("A", (0, 0)),
        (1, 0): Plant("A", (1, 0)),
        (2, 0): Plant("A", (2, 0)),
        (3, 0): Plant("A", (3, 0)),
        (0, 1): Plant("B", (0, 1)),
        (1, 1): Plant("B", (1, 1)),
        (2, 1): Plant("C", (2, 1)),
        (3, 1): Plant("D", (3, 1)),
        (0, 2): Plant("B", (0, 2)),
        (1, 2): Plant("B", (1, 2)),
        (2, 2): Plant("C", (2, 2)),
        (3, 2): Plant("C", (3, 2)),
        (0, 3): Plant("E", (0, 3)),
        (1, 3): Plant("E", (1, 3)),
        (2, 3): Plant("E", (2, 3)),
        (3, 3): Plant("C", (3, 3)),
    }

    cluster_expected = (
        (garden[(0, 0)], garden[(1, 0)], garden[(2, 0)], garden[(3, 0)]),
        (garden[(3, 1)],),
        (garden[(2, 1)], garden[(2, 2)], garden[(3, 2)], garden[(3, 3)]),
        (garden[(1, 2)], garden[(1, 1)], garden[(0, 2)], garden[(0, 1)]),
        (garden[(0, 3)], garden[(1, 3)], garden[(2, 3)]),
    )
    fences_expected = (10, 4, 10, 8, 8)
    sides_expected = (4, 4, 8, 4, 4)

    cluster_result, fences_result, sides_result = cluster_build(garden)

    assert cluster_result == cluster_expected
    assert fences_result == fences_expected
    assert sides_result == sides_expected


def test_part1() -> None:
    input = """
AAAA
BBCD
BBCC
EEEC
"""
    expected = 140

    assert part1(input) == expected

    input = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
    expected = 772

    assert part1(input) == expected

    input = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

    expected = 1930

    assert part1(input) == expected


def test_part2():
    input = """
AAAA
BBCD
BBCC
EEEC
"""
    expected = 80

    assert part2(input) == expected

    input = """
OOOOO
OXOXO
OOOOO
OXOXO
OOOOO
"""
    expected = 436

    assert part2(input) == expected

    input = """
EEEEE
EXXXX
EEEEE
EXXXX
EEEEE
"""
    expected = 236

    assert part2(input) == expected

    input = """
AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""
    expected = 368

    assert part2(input) == expected

    input = """
RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

    expected = 1206

    assert part2(input) == expected
