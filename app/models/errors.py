from typing import Optional

class HTTPResponse(Exception):
    def __init__(
        self,
        status_code: int,
        detail: Optional[str]):
        self.status_code = status_code
        self.detail = detail