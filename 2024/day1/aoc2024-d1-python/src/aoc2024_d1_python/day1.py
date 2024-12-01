from ast import literal_eval
from collections import Counter
from re import split
from sys import stdin


def similarity_score(pairs: tuple[tuple[int, int], ...]) -> int:
    alpha, beta = zip(*pairs)
    beta_counter = Counter(beta)

    return sum(item * beta_counter.get(item, 0) for item in alpha)


def total_distance1(pairs: tuple[tuple[int, int], ...]) -> int:
    alpha, beta = zip(*pairs)

    return sum(abs(a - b) for a, b in zip(sorted(alpha), sorted(beta)))


def parse_line(line: str) -> tuple[int, int]:
    alpha, beta = split(r"\s+", line.strip())

    return int(literal_eval(alpha)), int(literal_eval(beta))


def main() -> None:
    pairs = tuple(parse_line(line) for line in stdin)

    print("PYTHON:", total_distance1(pairs), similarity_score(pairs))


if __name__ == "__main__":
    main()
