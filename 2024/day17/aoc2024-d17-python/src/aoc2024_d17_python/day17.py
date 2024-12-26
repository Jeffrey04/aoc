from dataclasses import dataclass
from functools import partial, reduce
from sys import stdin
from typing import Generator


@dataclass
class Program:
    code: tuple[int, ...]
    pointer: int = 0


@dataclass
class Computer:
    A: int
    B: int
    C: int
    program: Program
    OUTPUT: tuple[int, ...] = ()


def check_program_is_halted(program: Program) -> bool:
    return program.pointer >= len(program.code)


def parse(input: str) -> Computer:
    def reducer(current: Computer, incoming: str) -> Computer:
        if incoming.startswith("Register A:"):
            return Computer(
                int(incoming.split(":")[-1].strip()),
                current.B,
                current.C,
                current.program,
            )
        elif incoming.startswith("Register B:"):
            return Computer(
                current.A,
                int(incoming.split(":")[-1].strip()),
                current.C,
                current.program,
            )
        elif incoming.startswith("Register C:"):
            return Computer(
                current.A,
                current.B,
                int(incoming.split(":")[-1].strip()),
                current.program,
            )
        elif incoming.startswith("Program:"):
            return Computer(
                current.A,
                current.B,
                current.C,
                parse_program(incoming.split(":")[-1].strip()),
            )
        else:
            return current

    return reduce(reducer, input.strip().splitlines(), Computer(0, 0, 0, Program(())))


def parse_program(input: str) -> Program:
    return Program(tuple(int(item) for item in input.strip().split(",")))


def evaluate_combo(computer: Computer, operand: int) -> int:
    match operand:
        case 0 | 1 | 2 | 3:
            return operand

        case 4:
            return computer.A

        case 5:
            return computer.B

        case 6:
            return computer.C

        case 7:
            raise Exception("Unimplemented")

        case _:
            raise Exception("Invalid opcode")


def program_advance_pointer(program: Program, value: int) -> Program:
    return Program(program.code, value)


def opcode_adv(computer: Computer, operand: int) -> Computer:
    return Computer(
        computer.A // (2**operand),
        computer.B,
        computer.C,
        program_advance_pointer(computer.program, computer.program.pointer + 2),
        computer.OUTPUT,
    )


def opcode_bxl(computer: Computer, operand: int) -> Computer:
    return Computer(
        computer.A,
        computer.B ^ operand,
        computer.C,
        program_advance_pointer(computer.program, computer.program.pointer + 2),
        computer.OUTPUT,
    )


def opcode_bst(computer: Computer, operand: int) -> Computer:
    return Computer(
        computer.A,
        operand % 8,
        computer.C,
        program_advance_pointer(computer.program, computer.program.pointer + 2),
        computer.OUTPUT,
    )


def opcode_jnz(computer: Computer, operand: int) -> Computer:
    return Computer(
        computer.A,
        computer.B,
        computer.C,
        program_advance_pointer(
            computer.program,
            (computer.program.pointer + 2) if computer.A == 0 else operand,
        ),
        computer.OUTPUT,
    )


def opcode_bxc(computer: Computer) -> Computer:
    return Computer(
        computer.A,
        computer.B ^ computer.C,
        computer.C,
        program_advance_pointer(computer.program, computer.program.pointer + 2),
        computer.OUTPUT,
    )


def opcode_out(computer: Computer, operand: int) -> Computer:
    return Computer(
        computer.A,
        computer.B,
        computer.C,
        program_advance_pointer(computer.program, computer.program.pointer + 2),
        computer.OUTPUT + (operand % 8,),
    )


def opcode_bdv(computer: Computer, operand: int) -> Computer:
    return Computer(
        computer.A,
        computer.A // (2**operand),
        computer.C,
        program_advance_pointer(computer.program, computer.program.pointer + 2),
        computer.OUTPUT,
    )


def opcode_cdv(computer: Computer, operand: int) -> Computer:
    return Computer(
        computer.A,
        computer.B,
        computer.A // (2**operand),
        program_advance_pointer(computer.program, computer.program.pointer + 2),
        computer.OUTPUT,
    )


def evaluate(computer: Computer) -> Computer:
    opcode, operand = computer.program.code[
        computer.program.pointer : computer.program.pointer + 2
    ]

    match opcode:
        case 0:
            return opcode_adv(computer, evaluate_combo(computer, operand))

        case 1:
            return opcode_bxl(computer, operand)

        case 2:
            return opcode_bst(computer, evaluate_combo(computer, operand))

        case 3:
            return opcode_jnz(computer, operand)

        case 4:
            return opcode_bxc(computer)

        case 5:
            return opcode_out(computer, evaluate_combo(computer, operand))

        case 6:
            return opcode_bdv(computer, evaluate_combo(computer, operand))

        case 7:
            return opcode_cdv(computer, evaluate_combo(computer, operand))

        case _:
            raise Exception("Invalid opcode")


def evaluate_loop(computer: Computer):
    i = 0
    while not check_program_is_halted(computer.program):
        i += 1
        if i == 10000000:
            raise Exception("Overflow")
        computer = evaluate(computer)

    return computer


def computer_replace_a(computer: Computer, a: int) -> Computer:
    return Computer(a, computer.B, computer.C, Program(computer.program.code))


def search(computer: Computer) -> int:
    if computer.program.code == (0, 3, 5, 4, 3, 0):
        new_a = int("".join(map(str, computer.program.code[:-1][::-1])), 8) * 8

        assert (
            evaluate_loop(computer_replace_a(computer, new_a)).OUTPUT
            == computer.program.code
        )

        return new_a

    elif computer.program.code == (2, 4, 1, 5, 7, 5, 1, 6, 0, 3, 4, 2, 5, 5, 3, 0):
        # print(8**16 - 8**15, "total range")
        return next(
            reduce(
                partial(match_n_digits, computer),
                range(1, 17),
                None,
            )  # type: ignore
        )[0]
    else:
        raise Exception("Not yet unbreak")


def match_n_digits(
    computer: Computer,
    cluster_previous: Generator[tuple[int, tuple[int, ...]], None, None] | None,
    n: int,
) -> Generator[tuple[int, tuple[int, ...]], None, None]:
    incoming = computer.program.code[-n:]

    for _, clusters in cluster_previous or [(None, ())]:
        idx_offset = (
            sum(
                c * (8**power)
                for c, power in zip(clusters, range(len(clusters), 0, -1))
            )
            if clusters
            else 0
        )

        for idx, new_a in enumerate(
            range(8 ** (n - 1) + idx_offset, (8 ** (n - 1) + idx_offset) + 8)
            if clusters
            else range(8**0, 8**1)
        ):
            result = evaluate_loop(computer_replace_a(computer, new_a))

            if result.OUTPUT == incoming:
                # logger.info(
                #    "match",
                #    n=n,
                #    a=new_a,
                #    result=result.OUTPUT,
                #    goal=computer.program.code,
                # )
                yield (new_a, clusters + ((idx + idx_offset) % 8,))


def part1(input: str) -> str:
    return ",".join(map(str, evaluate_loop(parse(input)).OUTPUT))


def part2(input: str) -> int:
    return search(parse(input))


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
