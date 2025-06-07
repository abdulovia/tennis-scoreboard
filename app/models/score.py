from dataclasses import asdict, dataclass, field
import json


@dataclass
class Game:
    # possible vals: 0-7 15 30 40 Ad -> using str
    player1: str
    player2: str

    @classmethod
    def from_dct(cls, dct):
        return cls(dct.get("player1"), dct.get("player2"))


@dataclass
class Set:
    player1: int
    player2: int

    @classmethod
    def from_dct(cls, dct):
        return cls(dct.get("player1"), dct.get("player2"))

    def is_tiebreak(self) -> bool:
        return self.player1 == 6 and self.player2 == 6


@dataclass
class Total:
    player1: int
    player2: int

    @classmethod
    def from_dct(cls, dct):
        return cls(dct.get("player1"), dct.get("player2"))


@dataclass
class Score:
    """
    Stores the full tennis match score

    total: number of sets won by player1 and player2
    sets: list of sets with number of games each player won
    game: points of the current game
    """

    total: Total = field(default_factory=lambda: Total(0, 0))
    sets: list[Set] = field(default_factory=lambda: [Set(0, 0)])
    game: Game = field(default_factory=lambda: Game("0", "0"))

    def to_str(self):
        return json.dumps(asdict(self))

    @classmethod
    def from_str(cls, score_str):
        dct = json.loads(score_str)
        return cls(
            Total.from_dct(dct.get("total")),
            [Set.from_dct(set_dct) for set_dct in dct.get("sets")],
            Game.from_dct(dct.get("game")),
        )
