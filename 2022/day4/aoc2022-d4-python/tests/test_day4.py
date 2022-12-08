from aoc2022_d4_python.day4 import (
    check_is_overlapping,
    check_is_subset,
    count_fully_contain,
    count_overlapping,
    split_pair,
    split_positions,
)

test_input = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
""".strip()


def test_split_positions() -> None:
    assert (set([2, 3, 4]), set([6, 7, 8])) == split_positions("2-4,6-8")


def test_split_pair() -> None:
    expected = (
        (set([2, 3, 4]), set([6, 7, 8])),
        (set([2, 3]), set([4, 5])),
        (set([5, 6, 7]), set([7, 8, 9])),
        (set([2, 3, 4, 5, 6, 7, 8]), set([3, 4, 5, 6, 7])),
        (set([6]), set([4, 5, 6])),
        (set([2, 3, 4, 5, 6]), set([4, 5, 6, 7, 8])),
    )

    assert expected == split_pair(test_input)


def test_check_is_subset() -> None:
    assert True == check_is_subset(*split_positions("2-8,3-7"))
    assert True == check_is_subset(*split_positions("6-6,4-6"))
    assert False == check_is_subset(*split_positions("2-4,6-8"))


def test_find_fully_contain() -> None:
    assert 2 == count_fully_contain(test_input)


def test_is_overlapping() -> None:
    assert False == check_is_overlapping(*split_positions("2-4,6-8"))
    assert False == check_is_overlapping(*split_positions("2-3,4-5"))
    assert True == check_is_overlapping(*split_positions("5-7,7-9"))
    assert True == check_is_overlapping(*split_positions("2-8,3-7"))
    assert True == check_is_overlapping(*split_positions("6-6,4-6"))
    assert True == check_is_overlapping(*split_positions("2-6,4-8"))


def test_find_overlapping() -> None:
    assert 4 == count_overlapping(test_input)
