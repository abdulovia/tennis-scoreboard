from dataclasses import asdict, dataclass
import json
from app.models.score import Score


@dataclass
class MatchDTO:
    uuid: str
    player1: str
    player2: str
    winner: str
    score: Score

    def to_dict(self):
        return asdict(self)

    @classmethod
    def from_str(cls, match_str):
        dct = json.loads(match_str)
        return cls.from_dict(dct)

    @classmethod
    def from_dict(cls, dct):
        return cls(
            dct.get("uuid"),
            dct.get("player1"),
            dct.get("player2"),
            dct.get("winner"),
            Score.from_dict(dct.get("score")),
        )
