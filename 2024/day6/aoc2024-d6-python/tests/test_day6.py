from aoc2024_d6_python.day6 import ROTATE_RIGHT, Board, Guard, parse, part1, part2


def test_guard_rotate() -> None:
    guard = Guard((0, 0))
    assert guard.direction == (0, -1)

    guard.rotate(ROTATE_RIGHT)
    assert guard.direction == (1, 0)

    guard.rotate(ROTATE_RIGHT)
    assert guard.direction == (0, 1)

    guard.rotate(ROTATE_RIGHT)
    assert guard.direction == (-1, 0)

    guard.rotate(ROTATE_RIGHT)
    assert guard.direction == (0, -1)


def test_parse() -> None:
    input = """
#
^
"""
    expected = Board(((0, 0),), Guard((0, 1)), (1, 2))

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
    expected = Board(
        (
            (4, 0),
            (9, 1),
            (2, 3),
            (7, 4),
            (1, 6),
            (8, 7),
            (0, 8),
            (6, 9),
        ),
        Guard((4, 6)),
        (10, 10),
    )

    assert parse(input) == expected


def test_in_board() -> None:
    board = Board((), Guard((0, 0)), (1, 1))

    input = (-1, 0)
    expected = False

    assert board.check_is_in_board(*input) == expected

    input = (0, -1)
    expected = False

    assert board.check_is_in_board(*input) == expected

    input = (-1, -1)
    expected = False

    assert board.check_is_in_board(*input) == expected

    input = (0, 1)
    expected = False

    assert board.check_is_in_board(*input) == expected

    input = (1, 0)
    expected = False

    assert board.check_is_in_board(*input) == expected

    input = (1, 1)
    expected = False

    assert board.check_is_in_board(*input) == expected

    input = (0, 0)
    expected = True

    assert board.check_is_in_board(*input) == expected


def test_check_is_obstruction() -> None:
    board = Board(((0, 0),), Guard((0, 1)), (1, 2))

    input = (0, 0)
    expected = True

    assert board.check_is_obstruction(*input) == expected

    input = (0, 1)
    expected = False

    assert board.check_is_obstruction(*input) == expected


def test_check_guard_can_move() -> None:
    board = Board(((0, 0),), Guard((0, 1)), (1, 2))

    expected = False

    assert board.check_guard_can_move() == expected

    board.guard.rotate(ROTATE_RIGHT)
    expected = True

    assert board.check_guard_can_move() == expected


def test_move_guard() -> None:
    board = Board(((0, 0),), Guard((0, 1)), (1, 2))
    assert board.guard.direction == (0, -1)
    assert board.guard.position == (0, 1)

    board.move_guard()
    assert board.guard.direction == (1, 0)
    assert board.guard.position == (0, 1)

    board.move_guard()
    assert board.guard.direction == (1, 0)
    assert board.guard.position == (1, 1)


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
