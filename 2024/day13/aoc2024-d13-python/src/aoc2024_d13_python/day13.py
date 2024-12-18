from functools import reduce
from sys import stdin

from toolz import merge

A = "A"
B = "B"
COST_A = 3
COST_B = 1


def extract_vector(input: str) -> tuple[int, int]:
    return tuple(int(item.strip().lstrip("X").lstrip("Y")) for item in input.split(","))  # type: ignore


def extract_point(input: str) -> tuple[int, int]:
    return tuple(
        int(item.strip().lstrip("X=").lstrip("Y=")) for item in input.split(",")
    )  # type: ignore


def parse(
    input: str, cost_a: int = COST_A, cost_b: int = COST_B
) -> tuple[tuple[dict[tuple[int, int], tuple[str, int]], tuple[int, int]], ...]:
    result = ()
    button, goal = {}, ()

    for line in input.strip().splitlines():
        if line.startswith("Button A:"):
            button[extract_vector(line.partition(":")[-1])] = (A, cost_a)
        elif line.startswith("Button B:"):
            button[extract_vector(line.partition(":")[-1])] = (B, cost_b)
        elif line.startswith("Prize:"):
            goal = extract_point(line.partition(":")[-1])
        else:
            result += ((button, goal),)

            button, goal = {}, ()

    return result + ((button, goal),)  # type: ignore


def move(current: tuple[int, int], incoming: tuple[int, int]) -> tuple[int, int]:
    return tuple((c + i) for c, i in zip(current, incoming))  # type: ignore


def move_set(
    current: tuple[int, int], button_count: dict[tuple[int, int], int]
) -> tuple[int, int]:
    return reduce(
        move,
        (
            (vector[0] * count, vector[1] * count)
            for vector, count in button_count.items()
        ),
        current,
    )


def cost_set(
    buttons: dict[tuple[int, int], tuple[str, int]],
    button_count: dict[tuple[int, int], int],
) -> int:
    return sum(buttons[vector][-1] * count for vector, count in button_count.items())


def find(
    buttons: dict[tuple[int, int], tuple[str, int]],
    goal: tuple[int, int],
    origin: tuple[int, int] = (0, 0),
) -> dict[int, tuple[dict[tuple[int, int], int], ...]]:
    result = {}
    candidates = [{vector: 1} for vector, (button, cost) in buttons.items()]

    while candidate := candidates.pop():
        print(candidate, len(candidates), len(result))

        for vector_incoming, (_, cost_incoming) in buttons.items():
            button_new = merge(
                candidate, {vector_incoming: candidate.get(vector_incoming, 0) + 1}
            )
            position_new = move_set(origin, button_new)

            if position_new == goal:
                print("found result")
                result[cost_set(buttons, button_new)] += result.get(
                    cost_set(buttons, button_new), ()
                ) + (button_new,)

            elif (
                check_is_past_goal(position_new, goal) or sum(button_new.values()) > 100
            ):
                print("exit early", position_new, button_new)
                continue

            elif button_new not in candidates:
                candidates.append(button_new)

    return result


def determinant(matrix: dict[tuple[int, int], int]) -> int:
    return matrix[(0, 0)] * matrix[(1, 1)] - matrix[(0, 1)] * matrix[(1, 0)]


def find2(
    buttons: dict[tuple[int, int], tuple[str, int]],
    goal: tuple[int, int],
    origin: tuple[int, int] = (0, 0),
) -> dict[tuple[int, int], int]:
    # apply cramer's rule
    # https://byjus.com/maths/cramers-rule/
    button_a, button_b = tuple(buttons.keys())
    result = {button_a: 0, button_b: 0}

    D = determinant(
        {
            (0, 0): button_a[0],
            (1, 0): button_a[1],
            (0, 1): button_b[0],
            (1, 1): button_b[1],
        }
    )
    Dx = determinant(
        {
            (0, 0): goal[0],
            (1, 0): goal[1],
            (0, 1): button_b[0],
            (1, 1): button_b[1],
        }
    )
    Dy = determinant(
        {
            (0, 0): button_a[0],
            (1, 0): button_a[1],
            (0, 1): goal[0],
            (1, 1): goal[1],
        }
    )

    if Dx % D == 0 and Dy % D == 0:
        result = {button_a: Dx // D, button_b: Dy // D}

    return result


def part1(input: str) -> int:
    return sum(
        buttons[button][-1] * count
        for buttons, goal in parse(input)
        for button, count in find2(buttons, goal).items()
    )


def part2(input: str) -> int:
    return sum(
        buttons[button][-1] * count
        for buttons, goal in parse(input)
        for button, count in find2(
            buttons,
            tuple(item + 10000000000000 for item in goal),  # type: ignore
        ).items()
    )


def check_is_past_goal(point: tuple[int, int], goal: tuple[int, int]) -> bool:
    return any(p > g for p, g in zip(point, goal))


def main():
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
