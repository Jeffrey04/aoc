from collections import Counter

import pytest

from aoc2024_d20_python.day20 import find_time_cheated, find_time_shortest, parse

input = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def test_find_time_shortest() -> None:
    race_track = parse(input)
    expected = 84

    assert find_time_shortest(race_track, race_track.end) == expected


@pytest.mark.skip()
def test_find_time_cheated() -> None:
    race_track = parse(input)
    expected = Counter(
        {
            2: 14,
            4: 14,
            6: 2,
            8: 4,
            10: 2,
            12: 3,
            20: 1,
            36: 1,
            38: 1,
            40: 1,
            64: 1,
        }
    )

    assert (
        Counter(value for value in find_time_cheated(race_track, 84).values())
        == expected
    )
