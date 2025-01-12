from __future__ import annotations

from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from functools import reduce
from itertools import combinations
from sys import stdin

from cytoolz.functoolz import memoize

CHIEF_STARTCHAR = "t"


@dataclass(frozen=True)
class Computer:
    name: str

    def __repr__(self) -> str:
        return self.name


@dataclass(frozen=True)
class Edge:
    source: Computer
    destination: Computer

    @property
    def inverse(self) -> Edge:
        return Edge(self.destination, self.source)


@dataclass(frozen=True)
class Network:
    computers: frozenset[Computer]
    edges: frozenset[Edge]

    @memoize
    def __contains__(self, edge: Edge) -> bool:
        assert isinstance(edge, Edge)

        return len({edge, edge.inverse} & self.edges) > 0


def parse(input: str) -> Network:
    def reducer(
        current: tuple[frozenset[Computer], frozenset[Edge]], incoming: str
    ) -> tuple[frozenset[Computer], frozenset[Edge]]:
        computers, edges = current
        source, dest = tuple(Computer(item) for item in incoming.split("-"))

        computers |= {source, dest}
        edges |= {Edge(source, dest)}

        return computers, edges

    return Network(
        *reduce(reducer, input.strip().splitlines(), (frozenset(), frozenset()))
    )


def build_parties(network: Network) -> Sequence[Sequence[Computer]]:
    parties = []

    for computer in sorted(network.computers, key=lambda item: item.name):
        found = None

        for idx, party in enumerate(parties):
            if check_party_interconnected(party + (computer,), network):
                parties.insert(idx, parties.pop(idx) + (computer,))
                found = True

        if not found:
            parties.append((computer,))

    return tuple(parties)


@memoize
def check_party_interconnected(party: Sequence[Computer], network: Network) -> bool:
    return all(
        Edge(source, destination) in network
        for source, destination in combinations(party, 2)
    )


def network_find_parties(
    network: Network, computer_count: int
) -> Iterator[tuple[Computer, ...]]:
    return (
        party
        for party in combinations(network.computers, computer_count)
        if check_party_interconnected(party, network)
    )


def check_party_has_chief(party: Sequence[Computer]) -> bool:
    return any(computer.name.startswith(CHIEF_STARTCHAR) for computer in party)


def parties_filter_chief(
    parties: Iterator[Sequence[Computer]],
) -> Iterator[Sequence[Computer]]:
    return (party for party in parties if check_party_has_chief(party))


def part1(input: str) -> int:
    return len(tuple(parties_filter_chief(network_find_parties(parse(input), 3))))


def part2(input: str) -> str:
    return ",".join(
        computer.name for computer in max(build_parties(parse(input)), key=len)
    )


def main() -> None:
    input = stdin.read()

    print("PYTHON:", part1(input), part2(input))


if __name__ == "__main__":
    main()
