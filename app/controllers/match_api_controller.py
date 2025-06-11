import json
from urllib.parse import parse_qsl
from app.services.match_service import MatchService
from app.models.response import Response


HEADER_JSON = ("Content-Type", "application/json")


class MatchApiController:
    service = MatchService()

    def get_match_score(self, query, body):
        dct = dict(parse_qsl(query))
        muuid = dct.get("uuid")
        if not muuid:
            message = json.dumps({"message": "uuid not found in query"})
            return Response(400, HEADER_JSON, message)
        match_dto = self.service.get_match_by_uuid(muuid)
        if not match_dto:
            message = json.dumps({"message": f"no match with this uuid"})
            return Response(404, HEADER_JSON, message)
        body = json.dumps(match_dto.to_dict())
        return Response(200, HEADER_JSON, body)

    def get_matches(self, query, body):
        dct = dict(parse_qsl(query))
        try:
            page = int(dct.get("page"))
        except ValueError:
            message = json.dumps({"message": "page must be integer"})
            return Response(400, HEADER_JSON, message)
        except Exception as e:
            page = None
        player_name = dct.get("filter_by_player_name")
        matches_dto_list = self.service.get_matches(page, player_name)
        if not matches_dto_list:
            message = json.dumps({"message": "no matches found"})
            return Response(404, HEADER_JSON, message)
        matches_dto = [match_dto.to_dict() for match_dto in matches_dto_list]
        body = json.dumps(matches_dto)
        return Response(200, HEADER_JSON, body)

    def post_new_match(self, query, body):
        dct = dict(parse_qsl(body))
        player1 = dct.get("player1")
        player2 = dct.get("player2")
        if not player1 or not player2:
            message = json.dumps({"message": "missing player in request body"})
            return Response(400, HEADER_JSON, message)
        match_dto = self.service.create_new_match(player1, player2)
        body = json.dumps(match_dto.to_dict())
        return Response(201, HEADER_JSON, body)

    def post_match_score(self, query, body):
        dct = dict(parse_qsl(query))
        muuid = dct.get("uuid")
        if not muuid:
            message = json.dumps({"message": "uuid not found in query"})
            return Response(400, HEADER_JSON, message)
        dct = dict(parse_qsl(body))
        point_winner = dct.get("point_winner")
        if not point_winner:
            message = json.dumps({"message": "missing point_winner in request body"})
            return Response(400, HEADER_JSON, message)
        match_dto = self.service.update_match_score(muuid, point_winner)
        if not match_dto:
            message = json.dumps({"message": "match score could not be updated"})
            return Response(404, HEADER_JSON, message)
        body = json.dumps(match_dto.to_dict())
        return Response(201, HEADER_JSON, body)
