from functools import reduce
from sys import stdin


def counter(elf_calories: str) -> int:
    return sum(map(int, elf_calories.strip().split("\n")))


def splitter(raw_calories: str) -> list[str]:
    return raw_calories.strip().split("\n\n")


def compile_input(raw_input: str) -> list[int]:
    return [counter(splitted) for splitted in splitter(raw_input)]


def find_most(elf_totals: list[int]) -> tuple[int, int]:
    idx_most = reduce(
        lambda current, incoming: current
        if elf_totals[current] > incoming[1]
        else incoming[0],
        enumerate(elf_totals),
        0,
    )

    return idx_most, elf_totals[idx_most]


def find_three(elf_totals: list[int]) -> tuple[tuple[int, int, int], int]:
    enum_totals = list(enumerate(elf_totals))

    result_zipped = sorted(enum_totals, key=lambda item: item[-1], reverse=True)[:3]

    return (
        tuple(idx for idx, _ in result_zipped),
        sum(calorie for _, calorie in result_zipped),
    )


def main() -> None:
    input_calories: list[int] = compile_input(stdin.read().strip())

    _idx, calories = find_most(input_calories)

    _idx_list, calories_total = find_three(input_calories)

    print(f"PYTHON: {calories} {calories_total}")


if __name__ == "__main__":
    main()
