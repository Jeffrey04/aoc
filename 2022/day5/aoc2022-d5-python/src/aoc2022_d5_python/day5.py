from functools import partial, reduce
from sys import stdin
from typing import Callable


def split_plan(plan_raw: str) -> tuple[str, str]:
    return tuple(plan_raw.split("\n\n"))


def parse_stack(stack_raw: str) -> list[list[str]]:
    result = []

    for line in stack_raw.splitlines():
        if not line.strip().startswith("["):
            break

        for idx_stack, idx_line in enumerate(range(0, len(line), 4)):
            if len(result) <= idx_stack:
                result.append([])

            container = line[idx_line : min(idx_line + 4, len(line))].strip()

            if container:
                result[idx_stack] = [container.strip("[]")] + result[idx_stack]

    return result


def parse_instruction(
    instruction_raw: str,
    mover: Callable[[list[list[str]], int, int, int], list[list[str]]],
) -> Callable[[list[list[str]]], list[list[str]]]:
    qty, origin, dest = tuple(
        int(token) for token in instruction_raw.split(" ") if token.isdigit()
    )
    return lambda current: mover(current, qty, origin - 1, dest - 1)


def move_stack(
    current: list[list[str]], qty: int, origin: int, dest: int
) -> list[list[str]]:
    for _ in range(qty):
        current[dest].append(current[origin].pop())

    return current


def move_stack2(
    current: list[list[str]], qty: int, origin: int, dest: int
) -> list[list[str]]:
    popped = []

    for _ in range(qty):
        popped.append(current[origin].pop())

    current[dest].extend(popped[::-1])

    return current


def check_stack_top(
    plan_raw: str,
    mover: Callable[[list[list[str]], int, int, int], list[list[str]]],
) -> str:
    stack_raw, instruction_raw = split_plan(plan_raw)

    result = reduce(
        lambda current, incoming: incoming(current),
        map(
            partial(parse_instruction, mover=mover),
            instruction_raw.strip().splitlines(),
        ),
        parse_stack(stack_raw),
    )

    return "".join(stack_sub[-1] for stack_sub in result)


def main() -> None:
    input_raw = stdin.read()

    print(
        f"PYTHON:\t{check_stack_top(input_raw, move_stack)} {check_stack_top(input_raw, move_stack2)}"
    )


if __name__ == "__main__":
    main()
