from aoc2022_d5_python.day5 import (
    check_stack_top,
    move_stack,
    move_stack2,
    parse_instruction,
    parse_stack,
    split_plan,
)

test_input = (
    """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3 \n\n"""
    """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""
)


def test_split_plan() -> None:
    plan = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3 """
    instruction = """move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

    assert (plan, instruction) == split_plan(test_input)


def test_parse_stack() -> None:
    plan = """    [D]
[N] [C]
[Z] [M] [P]
 1   2   3 """

    assert [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ] == parse_stack(plan)


def test_parse_instruction() -> None:
    plan = [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"],
    ]
    plan_expected = [
        ["Z", "N", "D"],
        ["M", "C"],
        ["P"],
    ]
    instruction_raw = "move 1 from 2 to 1"

    func = parse_instruction(instruction_raw, move_stack)

    assert plan_expected == func(plan)


def test_stack_top() -> None:
    assert "CMZ" == check_stack_top(test_input, move_stack)
    assert "MCD" == check_stack_top(test_input, move_stack2)
