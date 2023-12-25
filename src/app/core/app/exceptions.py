import http

from src.app.core.app.response import Response


class HTTPException(Response):
    def __init__(self, content: str = None, status_code: int = 400, headers: dict[str, str] | None = None) -> None:
        if content is None:
            content = http.HTTPStatus(status_code).phrase
        self.content = content
        super().__init__(content, status_code, headers)

    def __str__(self) -> str:
        return f'{self.status_code}: {self.content}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(status_code={self.status_code}, message={self.content})'
