from aoc2022_d6_python.day6 import (
    datastream_find_start_message,
    datastream_find_start_packet,
)

test_input = (
    "mjqjpqmgbljsphdztnvjfqwrcgsmlb",
    "bvwbjplbgvbhsrlpgdmjqwftvncz",
    "nppdvjthqldpwncqszvftbrmjlhg",
    "nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg",
    "zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw",
)


def test_find_start_packet() -> None:
    assert 7 == datastream_find_start_packet(test_input[0])
    assert 5 == datastream_find_start_packet(test_input[1])
    assert 6 == datastream_find_start_packet(test_input[2])
    assert 10 == datastream_find_start_packet(test_input[3])
    assert 11 == datastream_find_start_packet(test_input[4])


def test_find_start_message() -> None:
    assert 19 == datastream_find_start_message(test_input[0])
    assert 23 == datastream_find_start_message(test_input[1])
    assert 23 == datastream_find_start_message(test_input[2])
    assert 29 == datastream_find_start_message(test_input[3])
    assert 26 == datastream_find_start_message(test_input[4])
