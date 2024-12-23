from aoc2024_d16_python.day16 import find_path, parse, part1

input1 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

# result = find_path(*parse(input1))


with open("../input.txt", "r") as file:
    result = part1(file.read())

    print(result)

# def find_next(
#     trail: Trail, step: Point | Rotation, direction: Direction, maze: Maze
# ) -> tuple[list[tuple[Trail, Point | Rotation, Direction]], Trail | None]:
#     candidates, result = [], None
#
#     reindeer_current = tuple(step for step in trail if isinstance(step, Point))[-1]
#
#     if reindeer_current == maze.end:
#         result = trail
#         return candidates, result
#
#     destination = reindeer_current + direction
#
#     if check_can_move(maze, destination) and destination not in trail:
#         candidates.append(
#             (
#                 merge(trail, {destination: 1}),
#                 destination,
#                 direction,
#             )
#         )
#
#     if isinstance(step, Rotation):
#         return candidates, result
#
#     for rotation in (RotateLeft(), RotateRight()):
#         direction_rotated = rotate(direction, rotation)
#
#         if check_can_rotate(maze, reindeer_current, direction_rotated):
#             candidates.append(
#                 (
#                     merge_with(sum, trail, {rotation: 1}),
#                     rotation,
#                     direction_rotated,
#                 )
#             )
#
#     return candidates, result
#
#
# def find_path(
#     maze: Maze, reindeer: Point, direction_default: Direction = Direction(1, 0)
# ) -> Generator[Trail, None, None]:
#     candidates: list[tuple[Trail, Point | Rotation, Direction]] = [
#         ({reindeer: 1}, reindeer, direction_default)
#     ]
#
#     while True:
#         if len(candidates) < 20:
#             try:
#                 candidates_current, result = find_next(*candidates.pop(), maze=maze)
#             except IndexError:
#                 break
#
#             if result:
#                 yield result
#
#             candidates.extend(candidates_current)
#         else:
#             with ProcessPoolExecutor(max_workers=16) as executor:
#                 logger.info("go", candidates=len(candidates))
#                 tasks = []
#                 for trail, step, direction in candidates:
#                     tasks.append(
#                         executor.submit(find_next, trail, step, direction, maze)
#                     )
#
#                 candidates = []
#                 for task in tasks:
#                     candidates_new, result = task.result()
#
#                     if result:
#                         logger.info("Found result")
#                         yield result
#
#                     candidates.extend(candidates_new)
