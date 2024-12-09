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

    items: list[File | Space]

    def check_has_space(self) -> bool:
        return any(
            isinstance(item, File)
            for item in self.items[
                next(
                    (
                        idx
                        for idx, item in enumerate(self.items)
                        if isinstance(item, Space)
                    ),
                    len(self.items),
                ) :
            ]
        )

    def swap_block(self, alpha: int, beta: int) -> None:
        assert alpha < beta

        # sequence matters
        b, a = self.items.pop(beta), self.items.pop(alpha)

        # sequence matters
        self.items.insert(alpha, b)
        self.items.insert(beta, a)

    def move_block(self) -> None:
        assert self.check_has_space()

        self.swap_block(
            next(idx for idx, item in enumerate(self.items) if isinstance(item, Space)),
            len(self.items)
            + next(
                -1 - idx
                for idx, item in enumerate(self.items[::-1])
                if isinstance(item, File)
            ),
        )

    def compact_block(self) -> None:
        while True:
            try:
                self.move_block()
            except AssertionError:
                break

    def checksum(self) -> int:
        return sum(
            idx * item.id
            for idx, item in enumerate(self.items)
            if isinstance(item, File)
        )

    def find_file(self, file_id: int) -> int:
        return next(
            idx
            for idx, item in enumerate(self.items)
            if isinstance(item, File) and item.id == file_id
        )

    def find_space(self, length: int, max_search: int) -> int:
        return next(
            idx
            for idx, window in enumerate(
                sliding_window(length, self.items[:max_search])
            )
            if all(isinstance(item, Space) for item in window)
        )

    def move_file(self, file_id) -> None:
        file_idx = self.find_file(file_id)

        space_idx = self.find_space(self.map[file_id * 2], file_idx)

        for idx in range(self.map[file_id * 2]):
            self.swap_block(space_idx + idx, file_idx + idx)

    def compact_file(self) -> None:
        for file_id in reversed(
            tuple(idx // 2 for idx, size in enumerate(self.map) if idx % 2 == 0)
        ):
            try:
                self.move_file(file_id)
            except Exception:
                continue

    def __str__(self) -> str:
        return "".join(
            str(item.id) if isinstance(item, File) else "." for item in self.items
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
