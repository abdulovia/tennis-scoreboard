from sqlalchemy.orm import Session
from sqlalchemy import select, insert, update
from app.database.database import engine
from app.models.models import Match

PAGE_SIZE = 10


class MatchDAO:

    def get_match_by_uuid(self, muuid) -> Match | None:
        with Session(engine) as session:
            stmt = select(Match).where(Match.uuid == muuid)
            result = session.execute(stmt)
            return result.scalar_one_or_none()

    def create(self, muuid, p1_id, p2_id, score):
        with Session(engine) as session:
            match = Match(uuid=muuid, player1=p1_id, player2=p2_id, score=score)
            session.add(match)
            session.commit()
            session.refresh(match)
            return match

    def get_matches(self, page, player_id):
        with Session(engine) as session:
            stmt = select(Match).where(Match.winner.is_not(None))
            if player_id:
                stmt = stmt.where(
                    (Match.player1 == player_id) | (Match.player2 == player_id)
                )
            if page:
                stmt = stmt.offset((page - 1) * PAGE_SIZE).limit(PAGE_SIZE)
            result = session.execute(stmt)
            return result.scalars().all()

    def update(self, id, score, winner):
        with Session(engine) as session:
            match = session.get(Match, id)
            if not match:
                return None

            match.score = score
            if winner:
                match.winner = winner
                
            session.commit()
            session.refresh(match)
            return match
