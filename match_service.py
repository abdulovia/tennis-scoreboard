import logging
import uuid
from match_dao import MatchDAO
from match_dto import MatchDTO
from player_dao import PlayerDAO
from score_counter import ScoreUpdater
from score_dto import ScoreDTO


logger = logging.getLogger("match_service")

class MatchService:
    MatchDAO = MatchDAO()
    PlayerDAO = PlayerDAO()

    def __convert_to_match_dto(self, match):
        if match is None:
            logger.warning("__convert_to_match_dto got null match as param")
            return None
        p1 = self.PlayerDAO.get_player_by_id(match.player1)
        p2 = self.PlayerDAO.get_player_by_id(match.player2)
        winner = None
        if match.winner == p1.id:
            winner = p1.name
        elif match.winner == p2.id:
            winner = p2.name
        score = ScoreDTO.from_str(match.score)
        return MatchDTO(match.uuid, p1.name, p2.name, winner, score)

    def get_match_by_uuid(self, muuid):
        match = self.MatchDAO.get_match_by_uuid(muuid)
        if not match:
            return None
        match_dto = self.__convert_to_match_dto(match)
        return match_dto

    def get_matches(self, page, player_name):
        player_id = None
        if player_name:
            player = self.PlayerDAO.get_player_by_name(player_name)
            if not player:
                return None
            player_id = player.id
        matches = self.MatchDAO.get_matches(page, player_id)
        if not matches:
            return None
        matches_dto = []
        for match in matches:
            matches_dto.append(self.__convert_to_match_dto(match))
        return matches_dto

    def create_new_match(self, player1: str, player2: str):
        p1 = self.PlayerDAO.get_or_create(player1)
        p2 = self.PlayerDAO.get_or_create(player2)
        muuid = str(uuid.uuid4())
        score = ScoreDTO()
        match = self.MatchDAO.create(muuid, p1.id, p2.id, score.to_str())
        match_dto = self.__convert_to_match_dto(match)
        return match_dto

    def update_match_score(self, muuid, point_winner: str):
        match = self.MatchDAO.get_match_by_uuid(muuid)
        if not match:
            return None
        if match.winner:
            logger.warning(f"winner of match uuid={muuid} already exists")
            return None
        player = self.PlayerDAO.get_player_by_name(point_winner)
        if not player:
            return None
        score_dto = ScoreDTO.from_str(match.score)
        print(score_dto)
        su = ScoreUpdater(score_dto)
        if match.player1 == player.id:
            su.update_score(player1_winner=True)
        elif match.player2 == player.id:
            su.update_score(player1_winner=False)
        else:
            logger.warning("point_winner is neither player1 nor player2")
            return None
        winner = player.id if su.game_set_match() else None
        new_score = su.score
        match = self.MatchDAO.update(match.id, new_score.to_str(), winner)
        print(match)
        match_dto = self.__convert_to_match_dto(match)
        return match_dto
