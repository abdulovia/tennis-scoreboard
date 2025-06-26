from app.controllers.match_api_controller import MatchApiController
from app.controllers.match_view_controller import MatchViewController


class Router:
    api = MatchApiController()
    view = MatchViewController()
    routes = {
        "GET": {
            "/": view.get_index_page,
            "/new-match": view.get_new_match_page,
            "/match-score": view.get_match_score_page,
            "/matches": view.get_matches_page,
            "/static/css/style.css": view.get_style_css,
            "/api/match-score": api.get_match_score,
            "/api/matches": api.get_matches,
        },
        "POST": {
            "/new-match": view.post_new_match,
            "/match-score": view.post_match_score,
            "/api/new-match": api.post_new_match,
            "/api/match-score": api.post_match_score,
        },
    }

    def get_controller_method(self, http_method, path):
        return self.routes.get(http_method, {}).get(path, self.view.get_not_found_page)
