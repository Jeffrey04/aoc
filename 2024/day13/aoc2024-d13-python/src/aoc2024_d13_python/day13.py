from sys import stdin

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
) -> tuple[tuple[dict[tuple[int, int], int], tuple[int, int]], ...]:
    result = ()
    button, goal = {}, ()

    for line in input.strip().splitlines():
        if line.startswith("Button A:"):
            button[extract_vector(line.partition(":")[-1])] = cost_a
        elif line.startswith("Button B:"):
            button[extract_vector(line.partition(":")[-1])] = cost_b
        elif line.startswith("Prize:"):
            goal = extract_point(line.partition(":")[-1])
        else:
            result += ((button, goal),)

            button, goal = {}, ()

    return result + ((button, goal),)  # type: ignore


def determinant(matrix: dict[tuple[int, int], int]) -> int:
    return matrix[(0, 0)] * matrix[(1, 1)] - matrix[(0, 1)] * matrix[(1, 0)]


def find(
    buttons: dict[tuple[int, int], int],
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
        buttons[button] * count
        for buttons, goal in parse(input)
        for button, count in find(buttons, goal).items()
    )


def part2(input: str) -> int:
    return sum(
        buttons[button] * count
        for buttons, goal in parse(input)
        for button, count in find(
            buttons,
            tuple(item + 10000000000000 for item in goal),  # type: ignore
        ).items()
    )


def main():
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
