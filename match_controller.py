from urllib.parse import parse_qsl
from match_service import MatchService
from response import Response


class MatchController:
    ms = MatchService()

    def get_match_score(self, query):
        dct = dict(parse_qsl(query))
        muuid = dct.get("uuid")
        if not muuid:
            return Response(400, "Bad Request: uuid not found in query")
        match_dto = self.ms.get_match_by_uuid(muuid)
        if not match_dto:
            return Response(404, f"Not Found: no match with uuid={muuid}")
        return Response(200, "OK: match found", match_dto.to_dict())

    def get_matches(self, query):
        dct = dict(parse_qsl(query))
        try:
            page = int(dct.get("page"))
        except ValueError:
            return Response(400, "Bad Request: page must be integer")
        except Exception as e:
            page = None
        player_name = dct.get("filter_by_player_name")
        matches_dto_list = self.ms.get_matches(page, player_name)
        if not matches_dto_list:
            return Response(404, "Not Found: no matches")
        matches_dto = [match_dto.to_dict() for match_dto in matches_dto_list]
        return Response(200, "OK: all matches found", matches_dto)

    def post_new_match(self, query, data):
        dct = dict(parse_qsl(data))
        player1 = dct.get("player1")
        player2 = dct.get("player2")
        if not player1 or not player2:
            return Response(400, "Bad Request: missing player in post body")
        match_dto = self.ms.create_new_match(player1, player2)
        return Response(201, "OK: match created", match_dto.to_dict())

    def post_match_score(self, query, data):
        dct = dict(parse_qsl(query))
        muuid = dct.get("uuid")
        if not muuid:
            return Response(400, "Bad Request: uuid not found in query")
        dct = dict(parse_qsl(data))
        point_winner = dct.get("point_winner")
        if not point_winner:
            return Response(400, "Bad Request: missing point_winner key in post body")
        match_dto = self.ms.update_match_score(muuid, point_winner)
        if not match_dto:
            return Response(404, "Not Found: match score could not be updated")
        return Response(200, "OK: match score update", match_dto.to_dict())
