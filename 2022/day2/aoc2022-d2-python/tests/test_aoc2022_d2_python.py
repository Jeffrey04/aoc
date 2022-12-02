from aoc2022_d2_python.day2 import (
    match_score,
    round_evaluate1,
    round_evaluate2,
    round_list_split,
    round_score,
)

input_round_list = """
A Y
B X
C Z
"""


def test_round_list_split() -> None:
    expected = ["A Y", "B X", "C Z"]

    assert expected == round_list_split(input_round_list)


def test_round_score() -> None:
    assert 8 == round_score(round_evaluate1, "A Y")
    assert 1 == round_score(round_evaluate1, "B X")
    assert 6 == round_score(round_evaluate1, "C Z")

    assert 4 == round_score(round_evaluate2, "A Y")
    assert 1 == round_score(round_evaluate2, "B X")
    assert 7 == round_score(round_evaluate2, "C Z")


def test_match_score() -> None:
    assert 15 == match_score(round_evaluate1, input_round_list)

    assert 12 == match_score(round_evaluate2, input_round_list)
