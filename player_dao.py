from sqlalchemy.orm import Session
from sqlalchemy import select, insert
from database import engine
from models import Player


class PlayerDAO:

    def get_or_create(self, name):
        with Session(engine) as session:
            result = session.execute(select(Player).where(Player.name == name))
            player = result.scalar_one_or_none()
            if not player:
                player = Player(name=name)
                session.add(player)
                session.commit()
                session.refresh(player)
            return player

    def get_player_by_id(self, id):
        with Session(engine) as session:
            result = session.execute(select(Player).where(Player.id == id))
            return result.scalar_one_or_none()

    def get_player_by_name(self, name):
        with Session(engine) as session:
            result = session.execute(select(Player).where(Player.name == name))
            return result.scalar_one_or_none()

    def create(self, name):
        with Session(engine) as session:
            session.execute(insert(Player).values(name=name))
            session.commit()
