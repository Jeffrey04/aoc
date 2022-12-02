from sys import stdin

OPPONENT_ROCK = "A"
OPPONENT_PAPER = "B"
OPPONENT_SCISSORS = "C"

SELF_ROCK = "X"
SELF_PAPER = "Y"
SELF_SCISSORS = "Z"

SCORE_LOSE = 0
SCORE_DRAW = 3
SCORE_WIN = 6

HAND_SCORE_ROCK = 1
HAND_SCORE_PAPER = 2
HAND_SCORE_SCISSORS = 3

ROUND_LOSE = "X"
ROUND_DRAW = "Y"
ROUND_WIN = "Z"

RULE_WIN = {
    OPPONENT_ROCK: SELF_PAPER,
    OPPONENT_PAPER: SELF_SCISSORS,
    OPPONENT_SCISSORS: SELF_ROCK,
}
RULE_LOSE = {
    OPPONENT_ROCK: SELF_SCISSORS,
    OPPONENT_PAPER: SELF_ROCK,
    OPPONENT_SCISSORS: SELF_PAPER,
}
RULE_DRAW = {
    OPPONENT_ROCK: SELF_ROCK,
    OPPONENT_PAPER: SELF_PAPER,
    OPPONENT_SCISSORS: SELF_SCISSORS,
}


def round_evaluate1(round_record: str) -> tuple[str, int]:
    """
    Returns SCORE_*
    """
    result = SCORE_DRAW
    hand_opponent, hand_self = round_record.strip().split(" ")

    if RULE_WIN[hand_opponent] == hand_self:
        result = SCORE_WIN
    elif RULE_LOSE[hand_opponent] == hand_self:
        result = SCORE_LOSE

    return hand_self, result


def round_evaluate2(round_record: str) -> tuple[str, int]:
    rule_score = {ROUND_LOSE: SCORE_LOSE, ROUND_DRAW: SCORE_DRAW, ROUND_WIN: SCORE_WIN}

    hand_opponent, round_outcome = round_record.strip().split(" ")

    hand_self = RULE_DRAW[hand_opponent]

    if round_outcome == ROUND_LOSE:
        hand_self = RULE_LOSE[hand_opponent]

    elif round_outcome == ROUND_WIN:
        hand_self = RULE_WIN[hand_opponent]

    return hand_self, rule_score[round_outcome]


def round_score(scorer, round_record: str) -> int:
    hand_score = {
        SELF_ROCK: HAND_SCORE_ROCK,
        SELF_PAPER: HAND_SCORE_PAPER,
        SELF_SCISSORS: HAND_SCORE_SCISSORS,
    }

    hand_self, round_score = scorer(round_record)

    return hand_score[hand_self] + round_score


def round_list_split(round_list: str) -> list[str]:
    return round_list.strip().split("\n")


def match_score(scorer, round_list: str) -> int:
    return sum(
        round_score(scorer, round_record)
        for round_record in round_list_split(round_list)
    )


def main() -> None:
    input_raw = stdin.read()
    score_rule1 = match_score(round_evaluate1, input_raw)
    score_rule2 = match_score(round_evaluate2, input_raw)

    print(f"PYTHON:\t{score_rule1} {score_rule2}")


if __name__ == "__main__":
    main()
