from aoc2022_d1_python.day1 import (
    compile_input,
    counter,
    find_most,
    find_three,
    splitter,
)

input_text = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


def test_counter() -> None:
    expected = [6000, 4000, 11000, 24000, 10000]

    for i, grouped_calories in enumerate(splitter(input_text)):
        assert counter(grouped_calories) == expected[i]


def test_splitter() -> None:
    splitted = splitter(input_text)

    assert splitted == [
        "1000\n2000\n3000",
        "4000",
        "5000\n6000",
        "7000\n8000\n9000",
        "10000",
    ]


def test_find_most() -> None:
    idx, calories = find_most(compile_input(input_text))

    assert idx == 3
    assert calories == 24000


def test_find_three() -> None:
    idx_list, total = find_three(compile_input(input_text))

    assert idx_list == (3, 2, 4)
    assert total == 45000
