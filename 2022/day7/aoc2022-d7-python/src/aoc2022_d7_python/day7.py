from collections import namedtuple
from functools import partial, reduce
from sys import stdin
from typing import Optional

SIZE_TOTAL = 70000000
SIZE_MINIMUM = 30000000

Directory = namedtuple("Directory", ["children", "size"])


def is_command(input_line: str) -> bool:
    return input_line.startswith("$")


def input_build_tree(
    input_log,
    current_directory: Optional[str] = None,
    result: Optional[dict[str, Directory]] = None,
) -> dict[str, Directory]:
    if result is None:
        result = {}

    if len(input_log) != 0:
        command, output = input_log[0]

        result = input_build_tree(
            input_log[1:],
            cd_get_directory(command, current_directory or "")
            if check_command_is_cd(command)
            else current_directory,
            result
            if check_command_is_cd(command)
            else ls_update_result(output, current_directory or "", result),
        )

    return result


def check_command_is_cd(command: str) -> bool:
    return command.strip("$ ").startswith("cd")


def cd_get_directory(command: str, current_directory: str) -> str:
    result, target = None, command.split("cd")[-1].strip()

    if target == "/":
        result = "/"
    elif target == "..":
        result = current_directory.rsplit("/", 1)[0] or "/"
    else:
        result = path_build(current_directory, target)

    return result


def ls_update_result(
    output: tuple[str],
    current_directory: str,
    result: dict[str, Directory],
) -> dict[str, Directory]:
    path_prev, total_size, children = "", 0, ()

    for line in output:
        head, tail = line.split(" ")
        if check_output_is_dir(head):
            children = children + (path_build(current_directory, tail),)
        else:
            total_size += int(head)

    for path in directory_get_hierarchy(current_directory):
        if path_build(path_prev, path) not in result:
            result[path_build(path_prev, path)] = Directory(
                children=children, size=total_size
            )
        else:
            result[path_build(path_prev, path)] = Directory(
                children=result[path_build(path_prev, path)].children,
                size=result[path_build(path_prev, path)].size + total_size,
            )

        path_prev = path_build(path_prev, path)

    return result


def path_build(parent, directory) -> str:
    return f"{parent}/{directory}".replace("//", "/")


def directory_get_hierarchy(current_directory: str) -> list[str]:
    return (
        [current_directory]
        if current_directory == "/"
        else ["/"] + current_directory[1:].split("/")
    )


def check_output_is_dir(head) -> bool:
    return head == "dir"


def parse_input(input_raw: str) -> tuple[tuple[str, tuple[str]]]:
    result, current_command, cache = (), None, ()

    for line in input_raw.strip().splitlines():
        if is_command(line):
            if current_command:
                result = result + ((current_command, cache),)
                cache = ()

            current_command = line
        else:
            cache = cache + (line,)

    return result + ((current_command, cache),)


def calculate_total_size(input_raw: str) -> int:
    return sum(
        item.size
        for _, item in input_build_tree(parse_input(input_raw)).items()
        if item.size <= 100_000
    )


def compare_step2(
    current: Directory, incoming: Directory, space_free: int
) -> Directory:
    result = current

    delta_current = space_free + current.size
    delta_incoming = space_free + incoming.size

    if 30000000 <= delta_incoming < delta_current:
        result = incoming

    return result


def find_biggest_directory(input_raw: str) -> int:
    tree = input_build_tree(parse_input(input_raw))
    return reduce(
        partial(compare_step2, space_free=SIZE_TOTAL - tree["/"].size),
        tree.values(),
    ).size


def main() -> None:
    input_raw = stdin.read().strip()

    print(
        f"PYTHON:\t{calculate_total_size(input_raw)} "
        f"{find_biggest_directory(input_raw)}"
    )


if __name__ == "__main__":
    main()
