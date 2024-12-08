from aoc2024_d8_python.day8 import (
    Antenna,
    AntennaPair,
    find_antinodes,
    pair_antennas,
    parse,
    part1,
    part2,
    populate_antinodes,
)


def test_parse() -> None:
    input = """
..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........
"""
    expected = (10, 10), {"a": (Antenna(4, 3), Antenna(5, 5))}

    assert parse(input) == expected


def test_pair_antennas() -> None:
    input = (Antenna(4, 3), Antenna(5, 5), Antenna(1, 1))
    expected = (
        AntennaPair(Antenna(4, 3), Antenna(5, 5)),
        AntennaPair(Antenna(4, 3), Antenna(1, 1)),
        AntennaPair(Antenna(5, 5), Antenna(1, 1)),
    )

    assert pair_antennas(*input) == expected


def test_diff() -> None:
    input = AntennaPair(Antenna(4, 3), Antenna(5, 5))
    expected = (1, 2)

    assert input.diff() == expected

    input = AntennaPair(Antenna(5, 5), Antenna(8, 4))
    expected = (3, 1)


def test_find_antinodes() -> None:
    input = (AntennaPair(Antenna(4, 3), Antenna(5, 5)), (10, 10))
    expected = ((3, 1), (6, 7))

    assert find_antinodes(*input) == expected

    input = (AntennaPair(Antenna(5, 5), Antenna(8, 4)), (10, 10))
    expected = ((2, 6),)

    assert find_antinodes(*input) == expected


def test_part1():
    input = """
..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........
"""
    expected = 4

    assert part1(input) == expected

    input = """
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#."""
    expected = 14

    assert part1(input) == expected


def test_populate_antinodes() -> None:
    input = (AntennaPair(Antenna(0, 0), Antenna(3, 1)), (10, 10))
    expected = ((0, 0), (3, 1), (6, 2), (9, 3))

    assert populate_antinodes(*input) == expected


def test_part2() -> None:
    input = """
T....#....
...T......
.T....#...
.........#
..#.......
..........
...#......
..........
....#.....
..........
"""
    expected = 9

    assert part2(input) == expected

    input = """
......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#."""
    expected = 34

    assert part2(input) == expected
