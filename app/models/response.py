import json


class Response:
    def __init__(self, code: int, header: tuple, body: str):
        self.code = code
        self.header = header
        self.body = body

    def get_status(self) -> str:
        code_mapper = {
            200: "200 OK",
            201: "201 Created",
            302: "302 Found",
            400: "400 Bad Request",
            404: "404 Not Found",
            500: "500 Internal Server Error",
        }
        return code_mapper[self.code]
