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
) -> tuple[tuple[tuple[Plant, ...], ...], tuple[int, ...], tuple[int, ...]]:
    index, serial = {}, count(1)
    clusters, fences, corners = ((), (), ())

    candidates = [garden[0, 0]]

    while candidates:
        root = candidates.pop()

        if index.get(root.point):
            continue

        cluster = (root,)
        cluster_id = next(serial)

        index[root.point] = cluster_id

        corner_count = 0

        while True:
            neighbours_same = cluster_get_neighbours_same(garden, cluster)

            if not neighbours_same:
                break

            for current, incoming in neighbours_same:
                if index.get(incoming.point) is None:
                    cluster = cluster + (incoming,)
                    index[incoming.point] = cluster_id

        neighbours = cluster_get_neighbours_diff(garden, cluster)
        for point in set(
            neighbour.point
            for _, neighbour in neighbours
            if isinstance(neighbour, Plant)
        ):
            corner_count += inner_corner_count(garden, index, root, garden[point])

            if index.get(point) is None:
                candidates.append(garden[point])

        for plant in cluster:
            corner_count += outer_corner_count(garden, index, plant)

        clusters = clusters + (cluster,)
        fences = fences + (len(neighbours),)
        corners = corners + (corner_count,)

    return clusters, fences, corners

def inner_corner_count(
    garden: dict[tuple[int, int], Plant], index, root: Plant, plant: Plant
) -> int:
    up = check_if_same_type(root, garden.get((plant.point[0], plant.point[1] - 1)))
    down = check_if_same_type(root, garden.get((plant.point[0], plant.point[1] + 1)))
    left = check_if_same_type(root, garden.get((plant.point[0] - 1, plant.point[1])))
    right = check_if_same_type(root, garden.get((plant.point[0] + 1, plant.point[1])))
    tr = check_if_same_cluster(
        index,
        garden.get((plant.point[0] + 1, plant.point[1])),
        garden.get((plant.point[0], plant.point[1] - 1)),
    )
    br = check_if_same_cluster(
        index,
        garden.get((plant.point[0] + 1, plant.point[1])),
        garden.get((plant.point[0], plant.point[1] + 1)),
    )
    bl = check_if_same_cluster(
        index,
        garden.get((plant.point[0] - 1, plant.point[1])),
        garden.get((plant.point[0], plant.point[1] + 1)),
    )
    tl = check_if_same_cluster(
        index,
        garden.get((plant.point[0] - 1, plant.point[1])),
        garden.get((plant.point[0], plant.point[1] - 1)),
    )
    return len(
        tuple(
            filter(
                None,
                (
                    # top right
                    right and up and tr,
                    # bottom right
                    right and down and br,
                    # bottom left
                    left and down and bl,
                    # top left
                    left and up and tl,
                ),
            )
        )
    )

def check_if_same_cluster(
    index: dict[tuple[int, int], int], alpha: Plant | None, beta: Plant | None
) -> bool:
    if alpha is None and beta is None:
        return True

    try:
        if isinstance(alpha, Plant):
            return (
                isinstance(beta, Plant)
                and beta.point in index
                and index[alpha.point] == index[beta.point]
            )
        elif isinstance(beta, Plant):
            return (
                isinstance(alpha, Plant)
                and alpha.point in index
                and index[alpha.point] == index[beta.point]
            )
    except KeyError:
        return False


def outer_corner_count(
    garden: dict[tuple[int, int], Plant],
    index: dict[tuple[int, int], int],
    plant: Plant,
) -> int:
    up = check_if_same_type(plant, garden.get((plant.point[0], plant.point[1] - 1)))
    down = check_if_same_type(plant, garden.get((plant.point[0], plant.point[1] + 1)))
    left = check_if_same_type(plant, garden.get((plant.point[0] - 1, plant.point[1])))
    right = check_if_same_type(plant, garden.get((plant.point[0] + 1, plant.point[1])))
    tr = check_if_same_cluster(
        index, plant, garden.get((plant.point[0] + 1, plant.point[1] - 1))
    )
    br = check_if_same_cluster(
        index, plant, garden.get((plant.point[0] + 1, plant.point[1] + 1))
    )
    bl = check_if_same_cluster(
        index, plant, garden.get((plant.point[0] - 1, plant.point[1] + 1))
    )
    tl = check_if_same_cluster(
        index, plant, garden.get((plant.point[0] - 1, plant.point[1] - 1))
    )
    return len(
        tuple(
            filter(
                None,
                (
                    # top right
                    not right and not up and not tr,
                    # bottom right
                    not right and not down and not br,
                    # bottom left
                    not left and not down and not bl,
                    # top left
                    not left and not up and not tl,
                ),
            )
        )
    )


def check_if_same_type(alpha: Plant, beta: Plant | None) -> bool:
    return isinstance(beta, Plant) and alpha.name == beta.name


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


def cluster_get_neighbours_diff(
    garden: dict[tuple[int, int], Plant], cluster: tuple[Plant, ...]
) -> tuple[tuple[Plant, Plant | None], ...]:
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
            (neighbour is None)
            or (isinstance(neighbour, Plant) and neighbour.name != plant.name)
        )
    )


def part1(input: str) -> int:
    clusters, fences, _ = cluster_build(parse(input))

    return sum(len(cluster) * fences for cluster, fences in zip(clusters, fences))


def part2(input: str) -> int:
    clusters, _, sides = cluster_build(parse(input))

    return sum(len(cluster) * sides for cluster, sides in zip(clusters, sides))


def main():
    input = stdin.read()

    # part 2 is still wrong
    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
