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
            rules += (tuple(int(item) for item in incoming.strip().split("|")),)
        else:
            pages += (tuple(int(item) for item in incoming.strip().split(",")),)

        return rules, pages

    return reduce(
        inner, filter(lambda line: line.strip(), input.strip().splitlines()), ((), ())
    )


def check_pair(rules: tuple[tuple[int, int], ...], alpha: int, beta: int) -> bool:
    return ((beta, alpha) in rules) is False


def check_pages(rules: tuple[tuple[int, int], ...], pages: tuple[int, ...]) -> bool:
    def inner(current, incoming):
        pass

    return all(
        check_pair(rules, pages[idx], beta)
        # loop till second last
        for idx in range(len(pages) - 1)
        # inner loop from second element
        for beta in pages[idx + 1 :]
    )


def get_middle(pages: tuple[int, ...]) -> int:
    return pages[floor(len(pages) / 2)]


def move(items: tuple[int, ...], current: int, incoming: int):
    assert incoming > current

    result = list(items)
    result.insert(current, result.pop(incoming))

    return tuple(result)

def sort_pages(
    rules: tuple[tuple[int, int], ...], pages: tuple[int, ...], pointer: int = 0
) -> tuple[int, ...]:
    return (
        sort_pages(
            rules,
            *next(
                (
                    (move(pages, pointer, incoming), 0)
                    for incoming in range(pointer + 1, len(pages))
                    if check_pair(rules, pages[pointer], pages[incoming]) is False
                ),
                (pages, pointer + 1),
            ),
        )
        if pointer < (len(pages) - 1)
        else pages
    )


def part1(input: str) -> int:
    rules, pages_list = parse(input)

    return sum(get_middle(pages) for pages in pages_list if check_pages(rules, pages))


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
