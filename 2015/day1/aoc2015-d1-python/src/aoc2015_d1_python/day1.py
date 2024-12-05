from functools import reduce
from sys import stdin


def step(current: int, command: str) -> int:
    assert command in "()"

    match command:
        case "(":
            return current + 1

        case ")":
            return current - 1


def count(command: tuple[str, ...], current: int = 0, result: int = 0) -> int:
    assert len(command) > 0

    return (
        result
        if current == -1
        else count(
            command[1:],
            step(current, command[0]),
            result + 1,
        )
    )


def count2(command: tuple[str, ...]) -> int:
    current, result = 0, 0

    while True:
        if current == -1:
            return result

        current = step(current, command[result])
        result += 1


def part1(input: str) -> int:
    return reduce(step, tuple(input.strip()), 0)


def part2(input: str) -> int:
    return count2(tuple(input.strip()))


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
