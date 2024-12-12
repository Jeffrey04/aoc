import pytest

from aoc2024_d12_python.day12 import (
    Direction,
    Plant,
    cluster_build,
    cluster_get_neighbour_diff,
    cluster_get_neighbours_same,
    direction_merge_fences,
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
    expected = (garden[(0, 1)],)

    assert cluster_get_neighbour_diff(garden, input) == expected


def test_plant_merge_fence() -> None:
    input = (Direction.RIGHT, (True,) * 4, (True,) * 4)
    expected = (
        (False, True, True, True),
        (True, True, False, True),
    )

    assert direction_merge_fences(*input) == expected  # type: ignore


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

    cluster_expected = {
        1: (garden[(0, 0)], garden[(1, 0)], garden[(2, 0)], garden[(3, 0)]),
        2: (garden[(3, 1)],),
        3: (garden[(2, 1)], garden[(2, 2)], garden[(3, 2)], garden[(3, 3)]),
        4: (garden[(2, 3)], garden[(1, 3)], garden[(0, 3)]),
        5: (garden[(0, 2)], garden[(0, 1)], garden[(1, 2)], garden[(1, 1)]),
    }
    fences_expected = {
        # A
        (0, 0): (False, True, True, True),
        (1, 0): (False, True, False, True),
        (2, 0): (False, True, False, True),
        (3, 0): (True, True, False, True),
        # B
        (0, 1): (False, False, True, True),
        (1, 1): (True, False, False, True),
        (0, 2): (False, True, True, False),
        (1, 2): (True, True, False, False),
        # D
        (3, 1): (True, True, True, True),
        # C
        (2, 1): (True, False, True, True),
        (2, 2): (False, True, True, False),
        (3, 2): (True, False, False, True),
        (3, 3): (True, True, True, False),
        # E
        (0, 3): (False, True, True, True),
        (1, 3): (False, True, False, True),
        (2, 3): (True, True, False, True),
    }

    cluster_result, cluster_sides, fences_result = cluster_build(garden)

    assert cluster_result == cluster_expected
    assert fences_result == fences_expected


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

    assert part1(input) == expected
