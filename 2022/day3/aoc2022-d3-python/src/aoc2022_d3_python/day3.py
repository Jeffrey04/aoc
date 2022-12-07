import sys
from functools import reduce
from itertools import chain
from typing import Optional


def split_rucksack(item_list: str) -> tuple[str, str]:
    assert len(item_list) % 2 == 0

    mid_index = int(len(item_list) / 2)

    return item_list[:mid_index], item_list[mid_index:]


def find_common(item_list: tuple[str, ...]) -> Optional[str]:
    return "".join(
        reduce(
            lambda current, incoming: (current + (incoming,))
            if _find_common_check(current, incoming, item_list[1:])
            else current,
            tuple(item_list[0]),
            (),
        )
    )


def _find_common_check(current, incoming, reference_list) -> bool:
    return (incoming not in current) and all(
        incoming in reference for reference in reference_list
    )


def find_priority(item: str) -> int:
    assert len(item) == 1 and item.isalpha()

    code = ord(item)

    return code - 96 if item.lower() == item else code - 38


def find_sum_common(item_lists: str) -> int:
    return sum(
        map(
            find_priority,
            chain.from_iterable(
                tuple(find_common(split_rucksack(item_list)) or "")
                for item_list in item_lists.split("\n")
            ),
        )
    )


def split_groups(item_lists: str, size: int = 3) -> tuple[tuple[str, ...]]:
    rucksack_raw_list = tuple(item_lists.split("\n"))

    return tuple(
        rucksack_raw_list[start_idx : start_idx + size]
        for start_idx in range(0, len(rucksack_raw_list), size)
    )


def find_sum_badge(item_lists: str) -> int:
    return sum(
        find_priority(find_common(racksack_raw_group) or "")
        for racksack_raw_group in split_groups(item_lists)
    )


def main() -> None:
    input_raw = sys.stdin.read().strip()

    print(f"PYTHON:\t{find_sum_common(input_raw)} {find_sum_badge(input_raw)}")


if __name__ == "__main__":
    main()
