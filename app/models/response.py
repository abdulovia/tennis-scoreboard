import json


class Response:
    def __init__(self, code: int, message: str, body=None):
        self.code = code
        self.message = message
        self.body = body

    def to_str(self) -> str:
        if self.body is None:
            return json.dumps({"message": self.message})
        return json.dumps(self.body)

    def get_status(self) -> str:
        code_mapper = {
            200: "200 OK",
            201: "201 Created",
            400: "400 Bad Request",
            404: "404 Not Found",
            500: "500 Internal Server Error",
        }
        return code_mapper[self.code]
