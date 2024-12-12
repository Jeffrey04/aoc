from aoc2024_d6_python.day6 import (
    DIRECTION_DEFAULT,
    ROTATE_RIGHT,
    check_is_in_board,
    check_is_passable,
    guard_move,
    guard_rotate,
    parse,
    part1,
    part2,
)


def test_guard_rotate() -> None:
    input = (0, -1)

    direction = guard_rotate(input, ROTATE_RIGHT)
    assert direction == (1, 0)

    direction = guard_rotate(input, ROTATE_RIGHT)
    assert direction == (1, 0)

    direction = guard_rotate(input, ROTATE_RIGHT)
    assert direction == (1, 0)

    direction = guard_rotate(input, ROTATE_RIGHT)
    assert direction == (1, 0)


def test_parse() -> None:
    input = """
#
^
"""
    expected = {(0, 0): True}, (0, 1), (1, 2)

    assert parse(input) == expected

    input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    expected = (
        {
            (4, 0): True,
            (9, 1): True,
            (2, 3): True,
            (7, 4): True,
            (1, 6): True,
            (8, 7): True,
            (0, 8): True,
            (6, 9): True,
        },
        (4, 6),
        (10, 10),
    )

    assert parse(input) == expected


def test_in_board() -> None:
    dimension = (1, 1)

    input = (-1, 0)
    expected = False

    assert check_is_in_board(dimension, *input) == expected

    input = (0, -1)
    expected = False

    assert check_is_in_board(dimension, *input) == expected

    input = (-1, -1)
    expected = False

    assert check_is_in_board(dimension, *input) == expected

    input = (0, 1)
    expected = False

    assert check_is_in_board(dimension, *input) == expected

    input = (1, 0)
    expected = False

    assert check_is_in_board(dimension, *input) == expected

    input = (1, 1)
    expected = False

    assert check_is_in_board(dimension, *input) == expected

    input = (0, 0)
    expected = True

    assert check_is_in_board(dimension, *input) == expected


def test_check_is_passable() -> None:
    obstructions = {(0, 0): True}

    input = (0, 0)
    expected = False

    assert check_is_passable(obstructions, *input) == expected

    input = (0, 1)
    expected = True

    assert check_is_passable(obstructions, *input) == expected


def test_move_guard() -> None:
    guard = (0, 1)
    obstructions = {(0, 0): True}
    direction = DIRECTION_DEFAULT

    direction, guard = guard_move(guard, obstructions, direction, ROTATE_RIGHT)
    assert direction == (1, 0)
    assert guard == (0, 1)

    direction, guard = guard_move(guard, obstructions, direction, ROTATE_RIGHT)
    assert direction == (1, 0)
    assert guard == (1, 1)


def test_part1() -> None:
    input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    expected = 41

    assert part1(input) == expected


def test_part2() -> None:
    input = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""
    expected = 6

    assert part2(input) == expected
