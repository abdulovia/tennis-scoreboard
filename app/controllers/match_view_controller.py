import json
import math
from urllib.parse import parse_qsl, urlencode
from app.controllers.match_api_controller import MatchApiController
from app.models.match_dto import MatchDTO
from app.models.response import Response
from app.views.match_view import MatchView
from app.daos.match_dao import PAGE_SIZE


HEADER_HTML = ("Content-Type", "text/html")


class MatchViewController:
    view = MatchView()
    api = MatchApiController()

    def get_index_page(self, *args):
        body = self.view.render_index()
        return Response(200, HEADER_HTML, body)

    def get_new_match_page(self, *args):
        body = self.view.render_new_match()
        return Response(200, HEADER_HTML, body)

    def post_new_match(self, query, body):
        resp = self.api.post_new_match(query, body)
        if resp.code != 201:
            return Response(resp.code, HEADER_HTML, resp.body)
        match_dct = json.loads(resp.body)
        relative_path = f"/match-score?uuid={match_dct["uuid"]}"
        return Response(302, ("Location", relative_path), "")

    def get_match_score_page(self, query, body):
        resp = self.api.get_match_score(query, body)
        if resp.code != 200:
            return Response(resp.code, HEADER_HTML, resp.body)
        match_dto = MatchDTO.from_str(resp.body)
        body = self.view.render_match_score_page(match_dto)
        return Response(200, HEADER_HTML, body)

    def post_match_score(self, query, body):
        resp = self.api.post_match_score(query, body)
        if resp.code != 201:
            return Response(resp.code, HEADER_HTML, resp.body)
        match_dto = MatchDTO.from_str(resp.body)
        relative_path = f"/match-score?uuid={match_dto.uuid}"
        return Response(302, ("Location", relative_path), "")

    def get_matches_page(self, query, body):
        params = dict(parse_qsl(query))
        if not params.get("page"):
            params["page"] = 1
            query = urlencode(params)
            return Response(302, ("Location", "/matches?" + query), "")
        player_name = params.get("filter_by_player_name", "")
        resp = self.api.get_matches(query, body)
        if resp.code != 200:
            body = self.view.render_matches_page([], 0, player_name)
            return Response(200, HEADER_HTML, body)
        matches = json.loads(resp.body)
        matches_dto = [MatchDTO.from_dict(match) for match in matches]

        params.pop("page")
        query = urlencode(params)
        resp = self.api.get_matches(query, body)
        all_matches = json.loads(resp.body)
        pages = math.ceil(len(all_matches) / PAGE_SIZE)

        body = self.view.render_matches_page(matches_dto, pages, player_name)
        return Response(200, HEADER_HTML, body)

    def get_style_css(self, *args):
        body = self.view.render_style_css()
        return Response(200, ("Content-Type", "text/css"), body)

    def get_not_found_page(self, *args):
        body = self.view.render_not_found()
        return Response(200, HEADER_HTML, body)
