from functools import partial
from sys import stdin

START_PACKET_SIZE = 4
START_MESSAGE_SIZE = 14


def check_is_start_packet(idx: int, datastream: str, size: int = 4) -> bool:
    return not (
        idx < (size - 1)
        or any(
            len(datastream[idx - (size - 1) : idx + 1].split(character)) > 2
            for character in datastream[idx - (size - 1) : idx + 1]
        )
    )


def datastream_find_start_packet(datastream: str) -> int:
    return datastream_find_start(datastream, START_PACKET_SIZE)


def datastream_find_start_message(datastream: str) -> int:
    return datastream_find_start(datastream, START_MESSAGE_SIZE)


def datastream_find_start(datastream: str, size: int) -> int:
    return 1 + next(
        filter(
            partial(check_is_start_packet, size=size, datastream=datastream),
            range(len(datastream.strip())),
        )
    )


def main() -> None:
    input_raw = stdin.read().strip()

    print(
        f"PYTHON:\t{datastream_find_start_packet(input_raw)} "
        f"{datastream_find_start_message(input_raw)}"
    )


if __name__ == "__main__":
    main()
