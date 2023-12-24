import json
from typing import Any

from src.app.core.app.response import Response


class JSONResponse(Response):
    media_type = 'application/json'

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
    ) -> None:
        super().__init__(content, status_code, headers, media_type)

    def init_body(self, content: Any) -> bytes:
        return json.dumps(
            content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(',', ':'),
        ).encode(self.charset)
