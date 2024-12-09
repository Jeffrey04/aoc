from dataclasses import dataclass
from itertools import chain, repeat
from sys import stdin

from toolz import sliding_window


@dataclass
class File:
    id: int


@dataclass
class Space:
    pass


@dataclass
class Layout:
    map: tuple[int, ...]

    blocks: list[File | Space]

    def block_move(self) -> None:
        self.block_swap(
            self.space_find_first_idx(),
            self.file_find_last_idx(),
        )

    def block_swap(self, alpha: int, beta: int) -> None:
        assert alpha < beta

        # sequence matters
        b, a = self.blocks.pop(beta), self.blocks.pop(alpha)

        # sequence matters
        self.blocks.insert(alpha, b)
        self.blocks.insert(beta, a)

    def check_has_space_between_files(self) -> bool:
        return any(
            isinstance(item, File)
            for item in self.blocks[self.space_find_first_idx() :]
        )

    def checksum(self) -> int:
        return sum(
            idx * item.id
            for idx, item in enumerate(self.blocks)
            if isinstance(item, File)
        )

    def compact_block(self) -> None:
        while self.check_has_space_between_files():
            self.block_move()

    def compact_file(self) -> None:
        for file_id in range(len(self.map) // 2, -1, -1):
            try:
                self.file_move(file_id)
            except Exception:
                continue

    def file_find_first_idx(self, file_id: int) -> int:
        return next(
            idx
            for idx, item in enumerate(self.blocks)
            if isinstance(item, File) and item.id == file_id
        )

    def file_find_last_idx(self) -> int:
        return len(self.blocks) + next(
            -1 - idx
            for idx, item in enumerate(self.blocks[::-1])
            if isinstance(item, File)
        )

    def file_move(self, file_id: int) -> None:
        file_idx = self.file_find_first_idx(file_id)

        space_idx = self.space_find_idx_by_length(self.map[file_id * 2], file_idx)

        for idx in range(self.map[file_id * 2]):
            self.block_swap(space_idx + idx, file_idx + idx)

    def space_find_first_idx(self) -> int:
        return next(
            (idx for idx, item in enumerate(self.blocks) if isinstance(item, Space)),
            len(self.blocks),
        )

    def space_find_idx_by_length(self, length: int, max_search: int) -> int:
        first_space_idx = self.space_find_first_idx()

        return first_space_idx + next(
            idx
            for idx, window in enumerate(
                sliding_window(length, self.blocks[first_space_idx:max_search])
            )
            if all(isinstance(item, Space) for item in window)
        )

    def __str__(self) -> str:
        return "".join(
            str(item.id) if isinstance(item, File) else "." for item in self.blocks
        )


def parse(input: str) -> Layout:
    disk_map = tuple(int(item) for item in input)

    return Layout(
        disk_map,
        list(
            chain.from_iterable(
                repeat(File(int(idx / 2)) if (idx % 2) == 0 else Space(), item)
                for idx, item in enumerate(disk_map)
            )
        ),
    )


def part1(input: str) -> int:
    layout = parse(input.strip())

    layout.compact_block()

    return layout.checksum()


def part2(input: str) -> int:
    layout = parse(input.strip())

    layout.compact_file()

    return layout.checksum()


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
