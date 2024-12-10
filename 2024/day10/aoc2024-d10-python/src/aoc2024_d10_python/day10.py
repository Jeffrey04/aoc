from sys import stdin

TRAILHEAD_HEIGHT = 0
TRAILHEAD_MAX = 9


def parse(input: str) -> dict[tuple[int, int], int]:
    return {
        (x, y): int(item) if item.isdigit() else 99
        for y, row in enumerate(input.strip().splitlines())
        for x, item in enumerate(row)
    }


def next_step(
    topo_map: dict[tuple[int, int], int], x: int, y: int
) -> tuple[tuple[int, int], ...]:
    assert topo_map[(x, y)] != 9

    return tuple(
        incoming
        for incoming in (
            (x + 1, y),
            (x, y + 1),
            (x - 1, y),
            (x, y - 1),
        )
        if (
            isinstance(topo_map.get(incoming), int)
            and (topo_map[incoming] - topo_map[(x, y)] == 1)
        )
    )


def find_trailheads(
    topo_map: dict[tuple[int, int], int],
) -> tuple[tuple[int, int], ...]:
    return tuple(key for key, value in topo_map.items() if value == TRAILHEAD_HEIGHT)


def climb(
    topo_map: dict[tuple[int, int], int], trailheads: tuple[tuple[int, int], ...]
) -> dict[
    tuple[tuple[int, int], tuple[int, int]], tuple[tuple[tuple[int, int], ...], ...]
]:
    candidates: list[tuple[tuple[int, int], ...]] = [(head,) for head in trailheads]

    result = {}

    try:
        while current := candidates.pop():
            while True:
                if topo_map[current[-1]] == TRAILHEAD_MAX:
                    result[(current[0], current[-1])] = result.get(
                        (current[0], current[-1]), ()
                    ) + (current,)
                    break

                elif steps := next_step(topo_map, *current[-1]):
                    incoming, *rest = steps

                    candidates.extend([current + (step,) for step in rest])

                    current = current + (incoming,)
                else:
                    break
    except IndexError:
        pass

    return result


def part1(input: str) -> int:
    topo_map = parse(input)

    return len(climb(topo_map, find_trailheads(topo_map)))


def part2(input: str) -> int:
    topo_map = parse(input)

    print()

    return sum(
        len(routes) for routes in climb(topo_map, find_trailheads(topo_map)).values()
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
