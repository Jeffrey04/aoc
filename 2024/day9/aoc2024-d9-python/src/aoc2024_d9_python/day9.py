from dataclasses import dataclass
from itertools import chain, repeat
from sys import stdin

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

    def move_block(self) -> None:
        assert self.check_has_space()

        first_space = next(
            idx for idx, item in enumerate(self.items) if isinstance(item, Space)
        )

        self.items.append(self.items.pop(first_space))
        self.items.insert(
            first_space,
            self.items.pop(
                next(
                    -1 - idx
                    for idx, item in enumerate(self.items[::-1])
                    if isinstance(item, File)
                )
            ),
        )

    def compact(self) -> None:
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

    def find_space(self, length: int) -> int:
        # FIXME: cannot use self.map to find first current available space
        try:
            return sum(self.map[:next(idx for idx, item in enumerate(self.map) if (idx % 2) == 1 and length <= item)])
        except StopIteration as e:
            raise Exception('Cannot find space') from e

    def move_file(self, file_id) -> None:
        file_length = next(
            size for idx, size in enumerate(self.map) if idx % 2 == 0 and idx / 2 == file_id
        )

        # FIXME
        # self.find_space()


    def swap(self, file_id, space_id) -> None:
        pass

    def compact2() -> None:
        pass

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

    layout.compact()

    return layout.checksum()


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input))


if __name__ == "__main__":
    main()
