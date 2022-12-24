from aoc2022_d9_python.day9 import (
    DIRECTION_DOWN,
    DIRECTION_RIGHT,
    DIRECTION_UP,
    Rope,
    State,
    check_rope_is_touching,
    rope_calculate_visited,
    rope_move_head,
    rope_move_motion,
    rope_move_tail,
)


def test_check_rope_is_touching() -> None:
    assert True == check_rope_is_touching((1, 2), (1, 1))
    assert True == check_rope_is_touching((2, 1), (1, 2))
    assert True == check_rope_is_touching((1, 1), (1, 1))


def test_rope_move_tail() -> None:
    moved_right = rope_move_tail(Rope((1, 3), tail=(1, 1)), DIRECTION_RIGHT)

    assert ((1, 2), True) == moved_right.tail
    assert ((1, 3), False) == moved_right.head
    assert True == moved_right[(1, 1)]

    moved_down = rope_move_tail(Rope((1, 1), tail=(3, 1)), DIRECTION_DOWN)

    assert ((2, 1), True) == moved_down.tail
    assert ((1, 1), False) == moved_down.head
    assert True == moved_down[(3, 1)]

    moved_ur = rope_move_tail(Rope((3, 2), tail=(1, 1)), DIRECTION_UP)

    assert True == moved_ur[(1, 1)]
    assert False == moved_ur[(2, 1)]
    assert False == moved_ur[(1, 2)]
    assert ((2, 2), True) == moved_ur.tail
    assert ((3, 2), False) == moved_ur.head

    moved_ur2 = rope_move_tail(Rope((2, 3), tail=(1, 1)), DIRECTION_RIGHT)

    assert True == moved_ur2[(1, 1)]
    assert False == moved_ur2[(2, 1)]
    assert False == moved_ur2[(1, 2)]
    assert ((2, 2), True) == moved_ur2.tail
    assert ((2, 3), False) == moved_ur2.head


def test_rope_move_head() -> None:
    moved_right = rope_move_head(Rope((1, 2), tail=(1, 1)), DIRECTION_RIGHT)

    assert False == moved_right[(1, 2)]
    assert ((1, 3), False) == moved_right.head
    assert ((1, 1), True) == moved_right.tail


def test_rope_move_motion() -> None:
    moved = rope_move_motion(Rope((0, 0), chain=1), "R", 4)

    assert ((0, 0), True) == moved.start
    assert True == moved[(0, 0)]
    assert True == moved[(0, 1)]
    assert True == moved[(0, 2)]
    assert ((0, 3), True) == moved.tail
    assert ((0, 4), False) == moved.head


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

    assert 13 == rope_calculate_visited(Rope((0, 0), chain=1), test_input)
