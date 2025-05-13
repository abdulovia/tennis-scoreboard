from match_controller import MatchController
from response import Response


class Router:
    mc = MatchController()
    routes = {
        "GET": {
            "/match-score": mc.get_match_score,
            "/matches": mc.get_matches,
        },
        "POST": {
            "/new-match": mc.post_new_match,
            "/match-score": mc.post_match_score,
        },
    }

    def get_controller_method(self, http_method, path):
        return self.routes.get(http_method, {}).get(path, route_not_found)


def route_not_found(*args):
    return Response(404, "API Route Not Found")
