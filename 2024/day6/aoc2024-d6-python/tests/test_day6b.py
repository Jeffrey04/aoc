import pytest

from aoc2024_d6_python.day6b import (
    DIRECTION_DEFAULT,
    Board,
    Direction,
    Obstruction,
    Point,
    RotateRight,
    check_is_in_board,
    check_is_passable,
    guard_move,
    guard_rotate,
    parse,
    part1,
    part2,
)


def test_guard_rotate() -> None:
    input = Direction(0, -1)

    direction = guard_rotate(input, RotateRight())
    assert direction == Direction(1, 0)

    direction = guard_rotate(input, RotateRight())
    assert direction == Direction(1, 0)

    direction = guard_rotate(input, RotateRight())
    assert direction == Direction(1, 0)

    direction = guard_rotate(input, RotateRight())
    assert direction == Direction(1, 0)


def test_parse() -> None:
    input = """
#
^
"""
    expected = Board({Point(0, 0): Obstruction()}, 1, 2), Point(0, 1)

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
        Board(
            {
                Point(4, 0): Obstruction(),
                Point(9, 1): Obstruction(),
                Point(2, 3): Obstruction(),
                Point(7, 4): Obstruction(),
                Point(1, 6): Obstruction(),
                Point(8, 7): Obstruction(),
                Point(0, 8): Obstruction(),
                Point(6, 9): Obstruction(),
            },
            10,
            10,
        ),
        Point(4, 6),
    )

    assert parse(input) == expected


def test_in_board() -> None:
    board = Board({}, 1, 1)

    input = Point(-1, 0)
    expected = False

    assert check_is_in_board(board, input) == expected

    input = Point(0, -1)
    expected = False

    assert check_is_in_board(board, input) == expected

    input = Point(-1, -1)
    expected = False

    assert check_is_in_board(board, input) == expected

    input = Point(0, 1)
    expected = False

    assert check_is_in_board(board, input) == expected

    input = Point(1, 0)
    expected = False

    assert check_is_in_board(board, input) == expected

    input = Point(1, 1)
    expected = False

    assert check_is_in_board(board, input) == expected

    input = Point(0, 0)
    expected = True

    assert check_is_in_board(board, input) == expected


def test_check_is_passable() -> None:
    board = Board({Point(0, 0): Obstruction()}, 10, 10)

    input = Point(0, 0)
    expected = False

    assert check_is_passable(board, input) == expected

    input = Point(0, 1)
    expected = True

    assert check_is_passable(board, input) == expected


def test_move_guard() -> None:
    guard = Point(0, 1)
    board = Board({Point(0, 0): Obstruction()}, 10, 10)
    direction = DIRECTION_DEFAULT

    direction, guard = guard_move(board, guard, direction, RotateRight())
    assert direction == Direction(1, 0)
    assert guard == Point(0, 1)

    direction, guard = guard_move(board, guard, direction, RotateRight())
    assert direction == Direction(1, 0)
    assert guard == Point(1, 1)


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
