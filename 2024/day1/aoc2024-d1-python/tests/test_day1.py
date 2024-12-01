from aoc2024_d1_python.day1 import similarity_score, total_distance

input = ((3, 4), (4, 3), (2, 5), (1, 3), (3, 9), (3, 3))


def test_part1() -> None:
    expected = 11

    assert total_distance(input) == expected


def test_part2() -> None:
    expected = 31

    assert similarity_score(input) == expected
