import pytest

from aoc2024_d9_python.day9 import File, Layout, Space, parse, part1, part2

input = ("12345", "2333133121414131402")


def test_parse() -> None:
    expected = "0..111....22222"

    assert str(parse(input[0])) == expected

    expected = "00...111...2...333.44.5555.6666.777.888899"

    layout = parse(input[1])
    assert str(layout) == expected


def test_check_has_space() -> None:
    expected = True

    assert parse(input[0]).check_has_space() == expected

    expected = False

    assert parse("10305").check_has_space() == expected

    expected = False

    assert parse("103051").check_has_space() == expected


def test_move_block():
    layout = parse(input[0])

    expected = "02.111....2222."

    layout.move_block()
    assert str(layout) == expected

    expected = "022111....222.."

    layout.move_block()
    assert str(layout) == expected

    expected = "0221112...22..."

    layout.move_block()
    assert str(layout) == expected

    expected = "02211122..2...."

    layout.move_block()
    assert str(layout) == expected

    expected = "022111222......"

    layout.move_block()
    assert str(layout) == expected

    with pytest.raises(AssertionError):
        layout.move_block()

    layout = parse(input[1])

    expected = "009..111...2...333.44.5555.6666.777.88889."
    layout.move_block()
    assert str(layout) == expected

    expected = "0099.111...2...333.44.5555.6666.777.8888.."
    layout.move_block()
    assert str(layout) == expected

    expected = "00998111...2...333.44.5555.6666.777.888..."
    layout.move_block()
    assert str(layout) == expected

    expected = "009981118..2...333.44.5555.6666.777.88...."
    layout.move_block()
    assert str(layout) == expected

    expected = "0099811188.2...333.44.5555.6666.777.8....."
    layout.move_block()
    assert str(layout) == expected

    expected = "009981118882...333.44.5555.6666.777......."
    layout.move_block()
    assert str(layout) == expected

    expected = "0099811188827..333.44.5555.6666.77........"
    layout.move_block()
    assert str(layout) == expected

    expected = "00998111888277.333.44.5555.6666.7........."
    layout.move_block()
    assert str(layout) == expected

    expected = "009981118882777333.44.5555.6666..........."
    layout.move_block()
    assert str(layout) == expected

    expected = "009981118882777333644.5555.666............"
    layout.move_block()
    assert str(layout) == expected

    expected = "00998111888277733364465555.66............."
    layout.move_block()
    assert str(layout) == expected

    expected = "0099811188827773336446555566.............."
    layout.move_block()
    assert str(layout) == expected


def test_compact_block() -> None:
    layout = parse(input[0])

    expected = "022111222......"

    layout.compact_block()
    assert str(layout) == expected

    layout = parse(input[1])
    expected = "0099811188827773336446555566.............."

    layout.compact_block()
    assert str(layout) == expected


def test_part1() -> None:
    expected = 1928

    assert part1(input[1]) == expected


def test_find_space() -> None:
    layout = parse(input[1])
    expected = 2

    assert layout.find_space(2, len(layout.items)) == expected

    with pytest.raises(Exception):
        assert layout.find_space(10, len(layout.items)) == expected


def test_move_file() -> None:
    layout = parse(input[1])

    expected = "0099.111...2...333.44.5555.6666.777.8888.."

    layout.move_file(9)
    assert str(layout) == expected

    expected = "0099.1117772...333.44.5555.6666.....8888.."

    layout.move_file(7)
    assert str(layout) == expected

    expected = "0099.111777244.333....5555.6666.....8888.."

    layout.move_file(4)
    assert str(layout) == expected

    expected = "00992111777.44.333....5555.6666.....8888.."

    layout.move_file(2)
    assert str(layout) == expected


def test_part2() -> None:
    expected = 2858

    assert part2(input[1]) == expected
