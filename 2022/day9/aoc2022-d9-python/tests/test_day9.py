from aoc2022_d9_python.day9 import (DIRECTION_DOWN, DIRECTION_RIGHT,
                                    DIRECTION_UP, State,
                                    check_rope_is_touching,
                                    rope_calculate_visited, rope_init,
                                    rope_move_head, rope_move_motion,
                                    rope_move_tail)


def test_rope_init() -> None:
    expected = {
        1: {1: State(False, False, True, True), 2: State(False, True, False, False)}
    }

    assert expected == {
        row: {col: value for col, value in dict(_col).items()}
        for row, _col in dict(rope_init((1, 2), (1, 1))).items()
    }


def test_check_rope_is_touching() -> None:
    assert True == check_rope_is_touching(rope_init((1, 2), (1, 1)))
    assert True == check_rope_is_touching(rope_init((2, 1), (1, 2)))
    assert True == check_rope_is_touching(rope_init((1, 1)))


def test_rope_move_tail() -> None:
    moved_right = rope_move_tail(rope_init((1, 3), (1, 1)), DIRECTION_RIGHT)

    assert State(False, False, False, True) == moved_right[1][1]
    assert State(False, False, True, True) == moved_right[1][2]
    assert State(False, True, False, False) == moved_right[1][3]

    moved_down = rope_move_tail(rope_init((1, 1), (3, 1)), DIRECTION_DOWN)

    assert State(False, False, False, True) == moved_down[3][1]
    assert State(False, False, True, True) == moved_down[2][1]
    assert State(False, True, False, False) == moved_down[1][1]

    move_ur = rope_move_tail(rope_init((3, 2), (1, 1)), DIRECTION_UP)

    assert State(False, False, False, True) == move_ur[1][1]
    assert State(False, False, False, False) == move_ur[2][1]
    assert State(False, False, True, True) == move_ur[2][2]
    assert State(False, False, False, False) == move_ur[1][2]
    assert State(False, True, False, False) == move_ur[3][2]

    move_ur2 = rope_move_tail(rope_init((2, 3), (1, 1)), DIRECTION_RIGHT)

    assert State(False, False, False, True) == move_ur2[1][1]
    assert State(False, False, False, False) == move_ur2[2][1]
    assert State(False, False, True, True) == move_ur2[2][2]
    assert State(False, False, False, False) == move_ur2[1][2]
    assert State(False, True, False, False) == move_ur2[2][3]


def test_rope_move_head() -> None:
    moved_right = rope_move_head(rope_init((1, 2), (1, 1)), DIRECTION_RIGHT)

    assert State(False, False, False, False) == moved_right[1][2]
    assert State(False, True, False, False) == moved_right[1][3]
    assert State(False, False, True, True) == moved_right[1][1]


def test_rope_move_motion() -> None:
    moved = rope_move_motion(rope_init((0, 0), is_start=True), "R", 4)

    assert State(True, False, False, True) == moved[0][0]
    assert State(False, False, False, True) == moved[0][1]
    assert State(False, False, False, True) == moved[0][2]
    assert State(False, False, True, True) == moved[0][3]
    assert State(False, True, False, False) == moved[0][4]


def test_rope_calculate_visited() -> None:
    test_input = """
R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".strip()

    assert 13 == rope_calculate_visited(rope_init((0, 0), is_start=True), test_input)
