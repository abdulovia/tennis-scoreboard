from dataclasses import asdict, dataclass
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
