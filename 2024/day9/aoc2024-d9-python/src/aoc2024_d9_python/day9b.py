from functools import reduce
from itertools import chain, repeat
from sys import stdin

from toolz import sliding_window


def block_move(blocks: tuple[int | None, ...]) -> tuple[int | None, ...]:
    return block_swap(
        blocks,
        space_find_first_idx(blocks),
        file_find_last_idx(blocks),
    )


def block_swap(
    blocks: tuple[int | None, ...], alpha: int, beta: int
) -> tuple[int | None, ...]:
    assert alpha < beta

    return (
        *blocks[:alpha],
        blocks[beta],
        *blocks[alpha + 1 : beta],
        blocks[alpha],
        *blocks[beta + 1 :],
    )


def check_has_space_between_files(blocks: tuple[int | None, ...]) -> bool:
    return any(isinstance(item, int) for item in blocks[space_find_first_idx(blocks) :])


def checksum(blocks: tuple[int | None, ...]) -> int:
    return sum(idx * item for idx, item in enumerate(blocks) if isinstance(item, int))


def compact_block(blocks: tuple[int | None, ...]) -> tuple[int | None, ...]:
    # recursion will be super duper slow
    result = blocks

    while check_has_space_between_files(result):
        result = block_move(result)

    return result


def compact_file(
    disk_map: tuple[int, ...], blocks: tuple[int | None, ...]
) -> tuple[int | None, ...]:
    result = blocks

    for file_id in range(len(disk_map) // 2, -1, -1):
        try:
            result = file_move(disk_map, result, file_id)
        except Exception:
            continue

    return result


def file_find_first_idx(blocks: tuple[int | None, ...], file_id: int) -> int:
    return next(
        idx
        for idx, item in enumerate(blocks)
        if isinstance(item, int) and item == file_id
    )


def file_find_last_idx(blocks: tuple[int | None, ...]) -> int:
    return len(blocks) + next(
        -1 - idx for idx, item in enumerate(blocks[::-1]) if isinstance(item, int)
    )


def file_move(
    disk_map: tuple[int, ...], blocks: tuple[int | None, ...], file_id: int
) -> tuple[int | None, ...]:
    file_idx = file_find_first_idx(blocks, file_id)

    space_idx = space_find_idx_by_length(blocks, disk_map[file_id * 2], file_idx)

    return reduce(
        lambda current, idx: block_swap(current, space_idx + idx, file_idx + idx),
        range(disk_map[file_id * 2]),
        blocks,
    )


def parse(input: str) -> tuple[tuple[int, ...], tuple[int | None, ...]]:
    disk_map = tuple(int(item) for item in input)

    return disk_map, tuple(
        chain.from_iterable(
            repeat(idx // 2 if (idx % 2) == 0 else None, item)
            for idx, item in enumerate(disk_map)
        )
    )


def part1(input: str) -> int:
    _, blocks = parse(input.strip())

    return checksum(compact_block(blocks))


def part2(input: str) -> int:
    disk_map, blocks = parse(input.strip())

    return checksum(compact_file(disk_map, blocks))


def space_find_first_idx(blocks: tuple[int | None, ...]) -> int:
    return next(
        (idx for idx, item in enumerate(blocks) if item is None),
        len(blocks),
    )


def space_find_idx_by_length(
    blocks: tuple[int | None, ...], length: int, max_search: int
) -> int:
    first_space_idx = space_find_first_idx(blocks)
    return first_space_idx + next(
        idx
        for idx, window in enumerate(
            sliding_window(length, blocks[first_space_idx:max_search])
        )
        if all(item is None for item in window)
    )


def visualize(blocks: tuple[int | None, ...]) -> str:
    return "".join(str(item) if isinstance(item, int) else "." for item in blocks)


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
