import pytest

from aoc2024_d19_python.day19 import parse, part1, part2, pattern_match

input = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""


def test_parse() -> None:
    expected = (
        ("r", "wr", "b", "g", "bwu", "rb", "gb", "br"),
        (
            "brwrr",
            "bggr",
            "gbbr",
            "rrbgbr",
            "ubwu",
            "bwurrg",
            "brgr",
            "bbrgwb",
        ),
    )

    assert parse(input) == expected


@pytest.mark.skip()
def test_pattern_match() -> None:
    towels = ("r", "wr", "b", "g", "bwu", "rb", "gb", "br")

    pattern = "brwrr"
    expected = 2

    assert pattern_match(towels, pattern) == expected

    pattern = "bggr"
    expected = 1

    assert pattern_match(towels, pattern) == expected

    pattern = "gbbr"
    expected = 4

    assert pattern_match(towels, pattern) == expected

    pattern = "rrbgbr"
    expected = 6

    assert pattern_match(towels, pattern) == expected

    pattern = "ubwu"
    expected = 0

    assert pattern_match(towels, pattern) == expected

    pattern = "bwurrg"
    expected = 1

    assert pattern_match(towels, pattern) == expected

    pattern = "brgr"
    expected = 2

    assert pattern_match(towels, pattern) == expected

    pattern = "bbrgwb"
    expected = 0

    assert pattern_match(towels, pattern) == expected


def test_part1() -> None:
    expected = 6

    assert part1(input) == expected


def test_part2() -> None:
    expected = 16

    assert part2(input) == expected
