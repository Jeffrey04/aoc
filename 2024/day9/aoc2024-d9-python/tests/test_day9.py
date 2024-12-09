import pytest

from aoc2024_d9_python.day9 import parse, part1, part2

input = ("12345", "2333133121414131402")


def test_parse() -> None:
    expected = "0..111....22222"

    assert str(parse(input[0])) == expected

    expected = "00...111...2...333.44.5555.6666.777.888899"

    layout = parse(input[1])
    assert str(layout) == expected


def test_check_has_space() -> None:
    expected = True

    assert parse(input[0]).check_has_space_between_files() == expected

    expected = False

    assert parse("10305").check_has_space_between_files() == expected

    expected = False

    assert parse("103051").check_has_space_between_files() == expected


def test_move_block():
    layout = parse(input[0])

    expected = "02.111....2222."

    layout.block_move()
    assert str(layout) == expected

    expected = "022111....222.."

    layout.block_move()
    assert str(layout) == expected

    expected = "0221112...22..."

    layout.block_move()
    assert str(layout) == expected

    expected = "02211122..2...."

    layout.block_move()
    assert str(layout) == expected

    expected = "022111222......"

    layout.block_move()
    assert str(layout) == expected

    with pytest.raises(AssertionError):
        layout.block_move()

    layout = parse(input[1])

    expected = "009..111...2...333.44.5555.6666.777.88889."
    layout.block_move()
    assert str(layout) == expected

    expected = "0099.111...2...333.44.5555.6666.777.8888.."
    layout.block_move()
    assert str(layout) == expected

    expected = "00998111...2...333.44.5555.6666.777.888..."
    layout.block_move()
    assert str(layout) == expected

    expected = "009981118..2...333.44.5555.6666.777.88...."
    layout.block_move()
    assert str(layout) == expected

    expected = "0099811188.2...333.44.5555.6666.777.8....."
    layout.block_move()
    assert str(layout) == expected

    expected = "009981118882...333.44.5555.6666.777......."
    layout.block_move()
    assert str(layout) == expected

    expected = "0099811188827..333.44.5555.6666.77........"
    layout.block_move()
    assert str(layout) == expected

    expected = "00998111888277.333.44.5555.6666.7........."
    layout.block_move()
    assert str(layout) == expected

    expected = "009981118882777333.44.5555.6666..........."
    layout.block_move()
    assert str(layout) == expected

    expected = "009981118882777333644.5555.666............"
    layout.block_move()
    assert str(layout) == expected

    expected = "00998111888277733364465555.66............."
    layout.block_move()
    assert str(layout) == expected

    expected = "0099811188827773336446555566.............."
    layout.block_move()
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


def test_find_space_at_length() -> None:
    layout = parse(input[1])
    expected = 2

    assert layout.space_find_idx_by_length(2, len(layout.blocks)) == expected

    with pytest.raises(Exception):
        assert layout.space_find_idx_by_length(10, len(layout.blocks)) == expected


def test_move_file() -> None:
    layout = parse(input[1])

    expected = "0099.111...2...333.44.5555.6666.777.8888.."

    layout.file_move(9)
    assert str(layout) == expected

    expected = "0099.1117772...333.44.5555.6666.....8888.."

    layout.file_move(7)
    assert str(layout) == expected

    expected = "0099.111777244.333....5555.6666.....8888.."

    layout.file_move(4)
    assert str(layout) == expected

    expected = "00992111777.44.333....5555.6666.....8888.."

    layout.file_move(2)
    assert str(layout) == expected


def test_part2() -> None:
    expected = 2858

    assert part2(input[1]) == expected
