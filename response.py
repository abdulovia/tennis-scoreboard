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