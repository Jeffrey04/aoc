from functools import reduce
from math import floor
from sys import stdin


def parse(
    input: str,
) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, ...], ...]]:
    def inner(
        current, incoming
    ) -> tuple[tuple[tuple[int, int], ...], tuple[tuple[int, ...], ...]]:
        rules, pages = current

        if "|" in incoming:
            return rules + (
                tuple(int(item) for item in incoming.strip().split("|")),
            ), pages

        else:
            return rules, pages + (
                tuple(int(item) for item in incoming.strip().split(",")),
            )

    return reduce(
        inner, filter(lambda line: line.strip(), input.strip().splitlines()), ((), ())
    )


def check_pair(rules: tuple[tuple[int, int], ...], alpha: int, beta: int) -> bool:
    return (beta, alpha) not in rules


def check_pages(rules: tuple[tuple[int, int], ...], pages: tuple[int, ...]) -> bool:
    return all(
        check_pair(rules, pages[idx], beta)
        # loop till second last
        for idx in range(len(pages) - 1)
        # inner loop from second element
        for beta in pages[idx + 1 :]
    )


def get_middle(pages: tuple[int, ...]) -> int:
    return pages[floor(len(pages) / 2)]


def move(items: tuple[int, ...], current: int, incoming: int) -> tuple[int, ...]:
    assert incoming > current

    return (
        *items[:current],
        items[incoming],
        *tuple(
            item
            for idx, item in enumerate(items)
            if (idx >= current) and not (idx == incoming)
        ),
    )


def sort_pages(
    rules: tuple[tuple[int, int], ...],
    pages: tuple[int, ...],
    pointer: int = 0,
    subpointer: int = 0,
) -> tuple[int, ...]:
    return (
        sort_pages(
            rules,
            *next(
                (
                    (move(pages, pointer, incoming), pointer, pointer + 2)
                    for incoming in range(subpointer, len(pages))
                    if check_pair(rules, pages[pointer], pages[incoming]) is False
                ),
                (pages, pointer + 1, pointer + 2),
            ),
        )
        if pointer < (len(pages) - 1)
        else pages
    )


def part1(input: str) -> int:
    rules, pages_list = parse(input)

    return sum(
        get_middle(pages)
        # fmt: skip
        for pages in pages_list
        if check_pages(rules, pages)
    )


def part2(input: str) -> int:
    rules, pages_list = parse(input)

    return sum(
        get_middle(sort_pages(rules, pages))
        # fmt: skip
        for pages in pages_list
        if check_pages(rules, pages) is False
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
