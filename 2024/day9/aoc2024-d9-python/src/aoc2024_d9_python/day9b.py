from functools import reduce
from sys import stdin


def block_move(blocks: str) -> str:
    return block_swap(
        blocks,
        space_find_first_idx(blocks),
        file_find_last_idx(blocks),
    )


def block_swap(blocks: str, alpha: int, beta: int) -> str:
    assert alpha < beta

    return f"{blocks[:alpha]}{blocks[beta]}{blocks[alpha + 1 : beta]}{blocks[alpha]}{blocks[beta + 1 :]}"


def check_has_space_between_files(blocks: str) -> bool:
    return any(item.isdigit() for item in blocks[space_find_first_idx(blocks) :])


def checksum(blocks: str) -> int:
    return sum(idx * int(item) for idx, item in enumerate(blocks) if item.isdigit())


def compact_block(blocks: str) -> str:
    # recursion will be super duper slow
    result = blocks

    while check_has_space_between_files(result):
        result = block_move(result)

    return result


def compact_file(disk_map: tuple[int, ...], blocks: str) -> str:
    result = blocks

    for file_id in range(len(disk_map) // 2, -1, -1):
        try:
            result = file_move(disk_map, result, file_id)
        except Exception:
            continue

    return result


def file_find_first_idx(blocks: str, file_id: int) -> int:
    return blocks.index(str(file_id))


def file_find_last_idx(blocks: str) -> int:
    return len(blocks) + next(
        -1 - idx for idx, item in enumerate(blocks[::-1]) if item.isdigit()
    )


def file_move(disk_map: tuple[int, ...], blocks: str, file_id: int) -> str:
    file_idx = file_find_first_idx(blocks, file_id)

    space_idx = space_find_idx_by_length(blocks, disk_map[file_id * 2], file_idx)

    return reduce(
        lambda current, idx: block_swap(current, space_idx + idx, file_idx + idx),
        range(disk_map[file_id * 2]),
        blocks,
    )


def parse(input: str) -> tuple[tuple[int, ...], str]:
    disk_map = tuple(int(item) for item in input)

    return disk_map, "".join(
        (str(idx // 2) if (idx % 2) == 0 else ".") * item
        for idx, item in enumerate(disk_map)
    )


def part1(input: str) -> int:
    _, blocks = parse(input.strip())

    return checksum(compact_block(blocks))


def part2(input: str) -> int:
    disk_map, blocks = parse(input.strip())

    return checksum(compact_file(disk_map, blocks))


def space_find_first_idx(blocks: str) -> int:
    try:
        return blocks.index(".")
    except ValueError:
        return len(blocks)


def space_find_idx_by_length(blocks: str, length: int, max_search: int) -> int:
    first_space_idx = space_find_first_idx(blocks)

    return first_space_idx + blocks[first_space_idx:max_search].index("." * length)


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
