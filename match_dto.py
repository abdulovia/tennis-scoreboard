from dataclasses import asdict, dataclass
from score_dto import ScoreDTO


@dataclass
class MatchDTO:
    uuid: str
    player1: str
    player2: str
    winner: str
    score: ScoreDTO

    def to_dict(self):
        return asdict(self)
