import operator
from collections.abc import Callable
from itertools import pairwise
from sys import stdin


def parse_line(line: str) -> tuple[int, ...]:
    return tuple(int(item) for item in line.split(" "))


def sliding_window(items: tuple[int, ...]) -> tuple[tuple[int, int], ...]:
    return tuple(pairwise(items))


def check_is_increasing(pairs: tuple[tuple[int, int], ...]) -> bool:
    return all(check_pair(alpha, beta, operator.le) for alpha, beta in pairs)


def check_is_decreasing(pairs: tuple[tuple[int, int], ...]) -> bool:
    return all(check_pair(alpha, beta, operator.ge) for alpha, beta in pairs)


def check_pair(alpha: int, beta: int, comparator: Callable[[int, int], bool]) -> bool:
    return comparator(alpha, beta)


def check_diff(alpha: int, beta: int) -> bool:
    return 1 <= abs(alpha - beta) <= 3


def check_safety(pairs: tuple[tuple[int, int], ...]) -> bool:
    return (check_is_increasing(pairs) or check_is_decreasing(pairs)) and all(
        check_diff(*pair) for pair in pairs
    )


def remove_idx(items: tuple[int, ...], idx_unwanted: int) -> tuple[int, ...]:
    return tuple(item for idx, item in enumerate(items) if idx != idx_unwanted)


def apply_dampener(
    check: Callable[[tuple[tuple[int, int], ...]], bool],
) -> Callable[[tuple[int, ...]], bool]:
    def inner(items: tuple[int, ...]) -> bool:
        return any(
            check(sliding_window(remove_idx(items, idx))) for idx in range(len(items))
        )

    return inner


def counter(checker: Callable[[tuple[int, ...]], bool], input: str) -> int:
    return len(
        tuple(
            filter(
                lambda item: item,
                (checker(parse_line(line)) for line in input.strip().splitlines()),
            )
        )
    )


def safe_count(input: str) -> int:
    return counter(lambda incoming: check_safety(sliding_window(incoming)), input)


def safe_count_with_dampener(input: str) -> int:
    return counter(
        lambda incoming: (  # fmt: skip
            check_safety(sliding_window(incoming))
            or apply_dampener(check_safety)(incoming)
        ),
        input,
    )


def main():
    input = stdin.read()

    print("PYTHON:", safe_count(input), safe_count_with_dampener(input))


if __name__ == "__main__":
    main()
