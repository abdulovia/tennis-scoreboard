from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), index=True)

    def __repr__(self) -> str:
        return f"Player(id={self.id!r}, name={self.name!r})"


class Match(Base):
    __tablename__ = "matches"

    id: Mapped[int] = mapped_column(primary_key=True)
    uuid: Mapped[str] = mapped_column(String(255), unique=True)
    player1: Mapped[int] = mapped_column(ForeignKey("players.id"))
    player2: Mapped[int] = mapped_column(ForeignKey("players.id"))
    winner: Mapped[int] = mapped_column(ForeignKey("players.id"), nullable=True)
    score: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Match(id={self.id!r}, uuid={self.uuid!r}, player1={self.player1!r}, player2={self.player2!r}, winner={self.winner!r}, score={self.score!r})"
