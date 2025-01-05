from aoc2024_d21_python.day21 import (
    Action,
    Position,
    actions_to_string,
    code_to_actions,
    destination_get_actions,
    keypad_init_directional,
    keypad_init_numeric,
    part1,
)

input = """
029A
980A
179A
456A
379A
"""


def test_destination_get_actions() -> None:
    numeric_pad = keypad_init_numeric()
    input = ("0", numeric_pad.initial)
    expected_dest = Position(1, 3)
    expected_actions = "<A"
    result_dest, result_actions = destination_get_actions(numeric_pad, *input)

    assert result_dest == expected_dest
    assert len(result_actions) == 1
    assert actions_to_string(result_actions[0]) == expected_actions

    numeric_pad = keypad_init_numeric()
    input = ("2", result_dest)
    expected_dest = Position(1, 2)
    expected_actions = "^A"
    result_dest, result_actions = destination_get_actions(numeric_pad, *input)

    assert result_dest == expected_dest
    assert len(result_actions) == 1
    assert actions_to_string(result_actions[0]) == expected_actions

    numeric_pad = keypad_init_numeric()
    input = ("9", result_dest)
    expected_dest = Position(2, 0)
    expected_actions = (">^^A", "^^>A")
    result_dest, result_actions = destination_get_actions(numeric_pad, *input)

    assert result_dest == expected_dest
    assert len(result_actions) == len(expected_actions)
    assert actions_to_string(result_actions[0]) in expected_actions
    assert actions_to_string(result_actions[1]) in expected_actions

    numeric_pad = keypad_init_numeric()
    input = ("A", result_dest)
    expected_dest = Position(2, 3)
    expected_actions = "vvvA"
    result_dest, result_actions = destination_get_actions(numeric_pad, *input)

    assert result_dest == expected_dest
    assert len(result_actions) == 1
    assert actions_to_string(result_actions[0]) == expected_actions

    directional_pad = keypad_init_directional()
    input = (Action.Left, directional_pad.initial)
    expected_dest = Position(0, 1)
    expected_actions = "v<<A"
    result_dest, result_actions = destination_get_actions(directional_pad, *input)

    assert result_dest == expected_dest
    assert expected_actions in [
        actions_to_string(actions) for actions in result_actions
    ]

    input = (Action.Activate, result_dest)
    expected_dest = Position(2, 0)
    expected_actions = ">>^A"
    result_dest, result_actions = destination_get_actions(directional_pad, *input)

    assert result_dest == expected_dest
    assert expected_actions in [
        actions_to_string(actions) for actions in result_actions
    ]


# def test_code_press() -> None:
#    numeric_pad = keypad_init_numeric()
#    directional_pad = keypad_init_directional()
#    input = "029A"
#    expected_moves = "<A^A>^^AvvvA", "<A^A^>^AvvvA", "<A^A^^>AvvvA"
#
#    result = code_to_actions(
#        input,  # type: ignore
#    )
#    assert actions_to_string(result) in expected_moves


def test_code_to_actions() -> None:
    input = "029A"
    expected = 68

    assert len(code_to_actions(input, 2)) == expected  # type: ignore


def test_part1() -> None:
    expected = 126384

    assert part1(input) == expected
