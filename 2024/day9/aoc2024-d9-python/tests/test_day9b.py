import pytest

from aoc2024_d9_python.day9b import (
    block_move,
    check_has_space,
    compact_block,
    file_move,
    parse,
    part1,
    part2,
    space_find_idx_by_length,
    visualize,
)

input = ("12345", "2333133121414131402")


def test_parse() -> None:
    expected = "0..111....22222"

    disk_map, blocks = parse(input[0])
    assert disk_map == (1, 2, 3, 4, 5)
    assert visualize(blocks) == expected

    expected = "00...111...2...333.44.5555.6666.777.888899"

    disk_map, blocks = parse(input[1])
    assert visualize(blocks) == expected


def test_check_has_space() -> None:
    expected = True

    _, blocks = parse(input[0])
    assert check_has_space(blocks) == expected

    expected = False

    _, blocks = parse("10305")
    assert check_has_space(blocks) == expected

    expected = False

    _, blocks = parse("103051")
    assert check_has_space(blocks) == expected


def test_move_block():
    _, blocks = parse(input[0])

    expected = "02.111....2222."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "022111....222.."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "0221112...22..."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "02211122..2...."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "022111222......"

    assert visualize(blocks := block_move(blocks)) == expected

    with pytest.raises(AssertionError):
        block_move(blocks)

    _, blocks = parse(input[1])

    expected = "009..111...2...333.44.5555.6666.777.88889."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "0099.111...2...333.44.5555.6666.777.8888.."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "00998111...2...333.44.5555.6666.777.888..."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "009981118..2...333.44.5555.6666.777.88...."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "0099811188.2...333.44.5555.6666.777.8....."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "009981118882...333.44.5555.6666.777......."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "0099811188827..333.44.5555.6666.77........"

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "00998111888277.333.44.5555.6666.7........."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "009981118882777333.44.5555.6666..........."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "009981118882777333644.5555.666............"

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "00998111888277733364465555.66............."

    assert visualize(blocks := block_move(blocks)) == expected

    expected = "0099811188827773336446555566.............."

    assert visualize(blocks := block_move(blocks)) == expected


def test_compact_block() -> None:
    _, blocks = parse(input[0])

    expected = "022111222......"

    assert visualize(compact_block(blocks)) == expected

    _, blocks = parse(input[1])
    expected = "0099811188827773336446555566.............."

    assert visualize(compact_block(blocks)) == expected


def test_part1() -> None:
    expected = 1928

    assert part1(input[1]) == expected


def test_find_space_at_length() -> None:
    _, blocks = parse(input[1])
    expected = 2

    assert space_find_idx_by_length(blocks, 2, len(blocks)) == expected

    with pytest.raises(Exception):
        space_find_idx_by_length(blocks, 10, len(blocks))


def test_move_file() -> None:
    disk_map, blocks = parse(input[1])

    expected = "0099.111...2...333.44.5555.6666.777.8888.."

    assert visualize(blocks := file_move(disk_map, blocks, 9)) == expected

    expected = "0099.1117772...333.44.5555.6666.....8888.."

    assert visualize(blocks := file_move(disk_map, blocks, 7)) == expected

    expected = "0099.111777244.333....5555.6666.....8888.."

    assert visualize(blocks := file_move(disk_map, blocks, 4)) == expected

    expected = "00992111777.44.333....5555.6666.....8888.."

    assert visualize(blocks := file_move(disk_map, blocks, 2)) == expected


def test_part2() -> None:
    expected = 2858

    assert part2(input[1]) == expected
