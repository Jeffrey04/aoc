from collections import Counter

from aoc2024_d20_python.day20 import (
    find_best_track,
    find_time_cheated,
    find_time_cheated_new_rule,
    find_track_time,
    parse,
)

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

def test_find_track_time() -> None:
    expected = 84

    assert find_track_time(parse(input)) == expected


def test_find_time_shortest() -> None:
    race_track = parse(input)
    expected = 84

    assert find_best_track(race_track)[0] == expected


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
        Counter(
            value
            for _, value in find_time_cheated(
                race_track,
                *find_best_track(race_track, race_track.start, race_track.end),
            )
        )
        == expected
    )


def test_find_time_cheated_new() -> None:
    race_track = parse(input)
    expected = Counter(
        {
            50: 32,
            52: 31,
            54: 29,
            56: 39,
            58: 25,
            60: 23,
            62: 20,
            64: 19,
            66: 12,
            68: 14,
            70: 12,
            72: 22,
            74: 4,
            76: 3,
        }
    )

    assert (
        Counter(
            value
            for _, value in find_time_cheated_new_rule(
                race_track,
                *find_best_track(race_track, race_track.start, race_track.end),
            )
            # spacer
            if value >= 50
        )
        == expected
    )
