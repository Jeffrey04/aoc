from dataclasses import dataclass
from enum import Enum, auto
from itertools import count
from sys import stdin
from typing import Any


class Direction(Enum):
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()
    UP = auto()


@dataclass
class Plant:
    name: str
    point: tuple[int, int]


def cluster_build(
    garden: dict[tuple[int, int], Plant],
) -> tuple[
    dict[int, tuple[Plant, ...]],
    dict[int, dict[Direction, list[list[Plant]]]],
    dict[tuple[int, int], tuple[bool, bool, bool, bool]],
]:
    index, clusters, cluster_sides, serial = {}, {}, {}, count(1)
    fences = {point: (True, True, True, True) for point in garden.keys()}

    candidates = [garden[0, 0]]

    while candidates:
        root = candidates.pop()

        if index.get(root.point):
            continue

        cluster = (root,)
        cluster_id = next(serial)

        index[root.point] = cluster_id
        cluster_sides[cluster_id] = {
            Direction.RIGHT: [[root]],
            Direction.DOWN: [[root]],
            Direction.LEFT: [[root]],
            Direction.UP: [[root]],
        }

        while True:
            neighbours_same = cluster_get_neighbours_same(garden, cluster)

            if not neighbours_same:
                break

            for current, incoming in neighbours_same:
                if index.get(incoming.point) is None:
                    cluster = cluster + (incoming,)
                    index[incoming.point] = cluster_id

                direction = pair_get_direction(current, incoming)
                fences[current.point], fences[incoming.point] = direction_merge_fences(
                    direction,
                    fences[current.point],
                    fences[incoming.point],
                )
                cluster_sides[cluster_id] = sides_build(
                    cluster_sides[cluster_id],
                    current,
                    fences[current.point],
                    incoming,
                    fences[incoming.point],
                )

        clusters[cluster_id] = cluster

        for candidate in cluster_get_neighbour_diff(garden, cluster):
            if index.get(candidate.point) is None:
                candidates.append(candidate)

    return clusters, cluster_sides, fences


def sides_build(sides, current_plant, current_fence, incoming_plant, incoming_fence):
    print()
    print()
    print("pair", current_plant, incoming_plant)
    print("cleaning current", current_plant, current_fence)
    print("before", sides)
    if current_fence[0] is False:
        result = []

        for cluster in sides[Direction.RIGHT]:
            if current_plant == cluster[0]:
                result.append(cluster[1:])
            elif current_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif current_plant in cluster:
                idx = cluster.index(current_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.RIGHT] = list(filter(None, result))

    if current_fence[1] is False:
        result = []

        for cluster in sides[Direction.DOWN]:
            if current_plant == cluster[0]:
                result.append(cluster[1:])
            elif current_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif current_plant in cluster:
                idx = cluster.index(current_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.DOWN] = list(filter(None, result))

    if current_fence[2] is False:
        result = []

        for cluster in sides[Direction.LEFT]:
            if current_plant == cluster[0]:
                result.append(cluster[1:])
            elif current_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif current_plant in cluster:
                idx = cluster.index(current_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.LEFT] = list(filter(None, result))

    if current_fence[3] is False:
        result = []

        for cluster in sides[Direction.UP]:
            if current_plant == cluster[0]:
                result.append(cluster[1:])
            elif current_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif current_plant in cluster:
                idx = cluster.index(current_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.UP] = list(filter(None, result))
    print("after", sides)
    print()
    print("cleaning incoming", current_plant, current_fence)
    print("before", sides)
    if incoming_fence[0] is False:
        result = []

        for cluster in sides[Direction.RIGHT]:
            if incoming_plant == cluster[0]:
                result.append(cluster[1:])
            elif incoming_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif incoming_plant in cluster:
                idx = cluster.index(incoming_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.RIGHT] = list(filter(None, result))

    if incoming_fence[1] is False:
        result = []

        for cluster in sides[Direction.DOWN]:
            if incoming_plant == cluster[0]:
                result.append(cluster[1:])
            elif incoming_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif incoming_plant in cluster:
                idx = cluster.index(incoming_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.DOWN] = list(filter(None, result))

    if incoming_fence[2] is False:
        result = []

        for cluster in sides[Direction.LEFT]:
            if incoming_plant == cluster[0]:
                result.append(cluster[1:])
            elif incoming_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif incoming_plant in cluster:
                idx = cluster.index(incoming_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.LEFT] = list(filter(None, result))

    if incoming_fence[3] is False:
        result = []

        for cluster in sides[Direction.UP]:
            if incoming_plant == cluster[0]:
                result.append(cluster[1:])
            elif incoming_plant == cluster[-1]:
                result.append(cluster[:-1])
            elif incoming_plant in cluster:
                idx = cluster.index(incoming_plant)
                result.append(cluster[:idx])
                result.append(cluster[idx + 1 :])
            else:
                result.append(cluster)

        sides[Direction.UP] = list(filter(None, result))

    print("adding incoming", incoming_plant, incoming_fence)
    if incoming_fence[0]:
        result = []

        if current_fence[0]:
            for cluster in sides[Direction.RIGHT]:
                if current_plant == cluster[0]:
                    cluster.insert(0, incoming_plant)
                elif current_plant == cluster[-1]:
                    cluster.append(incoming_plant)
                elif incoming_plant == cluster[0] or incoming_plant == cluster[-1]:
                    continue

                result.append(cluster)
        else:
            if (
                any(incoming_plant in cluster for cluster in sides[Direction.RIGHT])
                is False
            ):
                result.append([incoming_plant])

            result.extend(sides[Direction.RIGHT])

        sides[Direction.RIGHT] = result

    if incoming_fence[1]:
        result = []

        if current_fence[1]:
            for cluster in sides[Direction.DOWN]:
                if current_plant == cluster[0]:
                    cluster.insert(0, incoming_plant)
                elif current_plant == cluster[-1]:
                    cluster.append(incoming_plant)
                elif incoming_plant == cluster[0] or incoming_plant == cluster[-1]:
                    continue

                result.append(cluster)
        else:
            if (
                any(incoming_plant in cluster for cluster in sides[Direction.DOWN])
                is False
            ):
                result.append([incoming_plant])

            result.extend(sides[Direction.DOWN])

        sides[Direction.DOWN] = result

    if incoming_fence[2]:
        result = []

        if current_fence[2]:
            for cluster in sides[Direction.LEFT]:
                if current_plant == cluster[0]:
                    cluster.insert(0, incoming_plant)
                elif current_plant == cluster[-1]:
                    cluster.append(incoming_plant)
                elif incoming_plant == cluster[0] or incoming_plant == cluster[-1]:
                    continue

                result.append(cluster)
        else:
            if (
                any(incoming_plant in cluster for cluster in sides[Direction.LEFT])
                is False
            ):
                result.append([incoming_plant])

            result.extend(sides[Direction.LEFT])

        sides[Direction.LEFT] = result

    if incoming_fence[3]:
        result = []

        if current_fence[3]:
            for cluster in sides[Direction.UP]:
                if current_plant == cluster[0]:
                    cluster.insert(0, incoming_plant)
                elif current_plant == cluster[-1]:
                    cluster.append(incoming_plant)
                elif incoming_plant == cluster[0] or incoming_plant == cluster[-1]:
                    continue

                result.append(cluster)
        else:
            if (
                any(incoming_plant in cluster for cluster in sides[Direction.UP])
                is False
            ):
                result.append([incoming_plant])

            result.extend(sides[Direction.UP])

        sides[Direction.UP] = result
    print()
    print("after", sides)

    return sides


def parse(input: str) -> dict[tuple[int, int], Plant]:
    return {
        (x, y): Plant(item, (x, y))
        for y, row in enumerate(input.strip().splitlines())
        for x, item in enumerate(row)
    }


def cluster_get_neighbours_same(
    garden: dict[tuple[int, int], Plant], cluster: tuple[Plant, ...]
) -> tuple[tuple[Plant, Plant], ...]:
    return tuple(
        (plant, neighbour)
        for plant in cluster
        for neighbour in (
            garden.get((plant.point[0], plant.point[1] - 1)),
            garden.get((plant.point[0], plant.point[1] + 1)),
            garden.get((plant.point[0] - 1, plant.point[1])),
            garden.get((plant.point[0] + 1, plant.point[1])),
        )
        if (
            isinstance(neighbour, Plant)
            and neighbour.name == plant.name
            and neighbour not in cluster
        )
    )


def cluster_get_neighbour_diff(
    garden: dict[tuple[int, int], Plant], cluster: tuple[Plant, ...]
) -> tuple[Plant, ...]:
    return tuple(
        neighbour
        for plant in cluster
        for neighbour in (
            garden.get((plant.point[0], plant.point[1] - 1)),
            garden.get((plant.point[0], plant.point[1] + 1)),
            garden.get((plant.point[0] - 1, plant.point[1])),
            garden.get((plant.point[0] + 1, plant.point[1])),
        )
        if (isinstance(neighbour, Plant) and neighbour.name != plant.name)
    )


def direction_merge_fences(
    direction: Direction,
    fence_alpha: tuple[bool, bool, bool, bool],
    fence_beta: tuple[bool, bool, bool, bool],
) -> tuple[tuple[bool, bool, bool, bool], tuple[bool, bool, bool, bool]]:
    match direction:
        case Direction.RIGHT:
            fence_alpha = fence_remove_right(*fence_alpha)
            fence_beta = fence_remove_left(*fence_beta)

        case Direction.DOWN:
            fence_alpha = fence_remove_down(*fence_alpha)
            fence_beta = fence_remove_up(*fence_beta)

        case Direction.LEFT:
            fence_alpha = fence_remove_left(*fence_alpha)
            fence_beta = fence_remove_right(*fence_beta)

        case Direction.UP:
            fence_alpha = fence_remove_up(*fence_alpha)
            fence_beta = fence_remove_down(*fence_beta)

    return fence_alpha, fence_beta


def pair_get_direction(alpha: Plant, beta: Plant) -> Direction:
    direction = (beta.point[0] - alpha.point[0]), (beta.point[1] - alpha.point[1])

    assert (
        alpha.point != beta.point
        and (direction[0] == 0 and abs(direction[1]) == 1)  # vertical
        or (abs(direction[0]) == 1 and direction[1] == 0)  # horizontal
    )

    if check_is_right(direction):
        return Direction.RIGHT
    elif check_is_down(direction):
        return Direction.DOWN
    elif check_is_left(direction):
        return Direction.LEFT
    elif check_is_up(direction):
        return Direction.UP
    else:
        raise Exception("Invalid direction")


def check_is_right(direction: tuple[int, int]) -> bool:
    return direction == (1, 0)


def check_is_down(direction: tuple[int, int]) -> bool:
    return direction == (0, 1)


def check_is_left(direction: tuple[int, int]) -> bool:
    return direction == (-1, 0)


def check_is_up(direction: tuple[int, int]) -> bool:
    return direction == (0, -1)


def fence_remove_right(
    _, down: bool, left: bool, up: bool
) -> tuple[bool, bool, bool, bool]:
    return (False, down, left, up)


def fence_remove_down(
    right, _: bool, left: bool, up: bool
) -> tuple[bool, bool, bool, bool]:
    return (right, False, left, up)


def fence_remove_left(
    right, down: bool, _: bool, up: bool
) -> tuple[bool, bool, bool, bool]:
    return (right, down, False, up)


def fence_remove_up(
    right, down: bool, left: bool, _: bool
) -> tuple[bool, bool, bool, bool]:
    return (right, down, left, False)


def part1(input: str) -> int:
    clusters, _, fences = cluster_build(parse(input))

    return sum(
        (
            # area
            len(cluster)
            # perimeter
            * sum(len(tuple(filter(None, fences[plant.point]))) for plant in cluster)
        )
        for cluster in clusters.values()
    )


def part2(input: str) -> int:
    clusters, sides, _ = cluster_build(parse(input))

    return sum(
        (
            # area
            len(cluster)
            # sides
            * sum(len(side) for side in sides[id].values())
        )
        for id, cluster in clusters.items()
    )


def main():
    input = stdin.read()

    print("PYTHON:", part1(input))


if __name__ == "__main__":
    main()
