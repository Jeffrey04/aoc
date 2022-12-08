from itertools import chain
from sys import stdin


def check_is_subset(set_alpha: set[int], set_beta: set[int]) -> bool:
    intersect = set_alpha & set_beta

    return intersect == set_alpha or intersect == set_beta


def check_is_overlapping(set_alpha: set[int], set_beta: set[int]) -> bool:
    return len(set_alpha & set_beta) > 0


def split_positions(input_raw: str) -> tuple[set[int], set[int]]:
    return tuple(
        set(range(position[0], position[1] + 1))
        for section_range in input_raw.split(",")
        for position in [tuple(map(int, section_range.split("-")))]
    )


def split_pair(input_raw: str) -> tuple[tuple[set[int], set[int]], ...]:
    return tuple(
        split_positions(pair_raw) for pair_raw in input_raw.strip().split("\n")
    )


def count_fully_contain(input_raw: str) -> int:
    return _count_relationship(input_raw, check_is_subset)


def count_overlapping(input_raw: str) -> int:
    return _count_relationship(input_raw, check_is_overlapping)


def _count_relationship(input_raw: str, checker) -> int:
    return sum([(1 if checker(*pair) else 0) for pair in split_pair(input_raw)])


def main() -> None:
    input_raw = stdin.read().strip()

    print(f"PYTHON:\t{count_fully_contain(input_raw)} {count_overlapping(input_raw)}")


if __name__ == "__main__":
    main()
