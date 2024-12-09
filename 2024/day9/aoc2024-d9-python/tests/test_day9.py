import pytest

from aoc2024_d9_python.day9 import File, Layout, Space, parse, part1


def test_parse() -> None:
    input = "12345"
    expected = Layout(
        tuple(int(item) for item in input),
        [
            File(0),
            Space(),
            Space(),
            File(1),
            File(1),
            File(1),
            Space(),
            Space(),
            Space(),
            Space(),
            File(2),
            File(2),
            File(2),
            File(2),
            File(2),
        ],
    )

    assert parse(input) == expected

    input = "2333133121414131402"
    expected = "00...111...2...333.44.5555.6666.777.888899"

    layout = parse(input)
    assert str(layout) == expected


def test_check_has_space() -> None:
    input = Layout(
        (1, 2, 3, 4, 5),
        [
            File(0),
            Space(),
            Space(),
            File(1),
            File(1),
            File(1),
            Space(),
            Space(),
            Space(),
            Space(),
            File(2),
            File(2),
            File(2),
            File(2),
            File(2),
        ],
    )
    expected = True

    assert input.check_has_space() == expected

    input = Layout(
        (1, 0, 3, 0, 5),
        [
            File(0),
            File(1),
            File(1),
            File(1),
            File(2),
            File(2),
            File(2),
            File(2),
            File(2),
        ],
    )
    expected = False

    assert input.check_has_space() == expected

    input = Layout(
        (1, 0, 3, 0, 5, 1),
        [
            File(0),
            File(1),
            File(1),
            File(1),
            File(2),
            File(2),
            File(2),
            File(2),
            File(2),
            Space(),
        ],
    )
    expected = False

    assert input.check_has_space() == expected


def test_move_block():
    layout = Layout(
        (1, 2, 3, 4, 5),
        [
            File(0),
            Space(),
            Space(),
            File(1),
            File(1),
            File(1),
            Space(),
            Space(),
            Space(),
            Space(),
            File(2),
            File(2),
            File(2),
            File(2),
            File(2),
        ],
    )

    expected = [
        File(0),
        File(2),
        Space(),
        File(1),
        File(1),
        File(1),
        Space(),
        Space(),
        Space(),
        Space(),
        File(2),
        File(2),
        File(2),
        File(2),
        Space(),
    ]

    layout.move_block()
    assert layout.items == expected

    expected = [
        File(0),
        File(2),
        File(2),
        File(1),
        File(1),
        File(1),
        Space(),
        Space(),
        Space(),
        Space(),
        File(2),
        File(2),
        File(2),
        Space(),
        Space(),
    ]

    layout.move_block()
    assert layout.items == expected

    layout.move_block()
    layout.move_block()
    layout.move_block()

    with pytest.raises(AssertionError):
        layout.move_block()

    input = "2333133121414131402"
    layout = parse(input)

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


def test_compact() -> None:
    layout = Layout(
        (1, 2, 3, 4, 5),
        [
            File(0),
            Space(),
            Space(),
            File(1),
            File(1),
            File(1),
            Space(),
            Space(),
            Space(),
            Space(),
            File(2),
            File(2),
            File(2),
            File(2),
            File(2),
        ],
    )

    expected = [
        File(0),
        File(2),
        File(2),
        File(1),
        File(1),
        File(1),
        File(2),
        File(2),
        File(2),
        Space(),
        Space(),
        Space(),
        Space(),
        Space(),
        Space(),
    ]

    layout.compact()
    assert layout.items == expected

    input = "2333133121414131402"
    layout = parse(input)
    expected = "0099811188827773336446555566.............."

    layout.compact()
    assert str(layout) == expected


def test_part1() -> None:
    input = "2333133121414131402"
    expected = 1928

    assert part1(input) == expected


def test_find_space() -> None:
    input = "2333133121414131402"
    layout = parse(input)
    expected = 2

    assert layout.find_space(3) == expected

    with pytest.raises(Exception):
        assert layout.find_space(10) == expected


def test_move_file() -> None:
    input = "2333133121414131402"
    layout = parse(input)

    expected = '0099.111...2...333.44.5555.6666.777.8888..'

    layout.move_file(9)
    assert str(layout) == expected

    expected = '0099.1117772...333.44.5555.6666.....8888..'

    layout.move_file(7)
    assert str(layout) == expected

    expected = '0099.111777244.333....5555.6666.....8888..'

    layout.move_file(4)
    assert str(layout) == expected

    expected = '00992111777.44.333....5555.6666.....8888..'

    layout.move_file(2)
    assert str(layout) == expected



def test_part2() -> None:
    input = "2333133121414131402"
    expected = 2858

    assert part1(input) == expected