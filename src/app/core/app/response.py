from typing import Any


class Response:
    charset = 'utf-8'
    media_type = 'text/plain'

    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
        media_type: str | None = None,
    ) -> None:
        self.body = self.init_body(content)
        self.status_code = status_code
        self.media_type = media_type or self.media_type
        self.headers = headers
        self.raw_headers = self.init_headers(headers)

    def init_body(self, content: Any) -> bytes:
        if content is None:
            return b''
        if isinstance(content, bytes):
            return content
        return content.encode(self.charset)

    def init_headers(self, headers: dict[str, str] | None) -> list[list[bytes]]:
        if headers is None:
            raw_headers = []
        else:
            raw_headers = [[key.encode(self.charset), value.encode(self.charset)] for key, value in headers.items()]
        key_set = {key.lower() for key, _ in raw_headers}
        if self.body and b'content-length' not in key_set:
            raw_headers.append([b'Content-Length', str(len(self.body)).encode(self.charset)])
        if self.media_type and b'content-type' not in key_set:
            content_type = self.media_type
            if content_type.startswith('text/') and 'charset' not in content_type:
                content_type += f'; charset={self.charset}'
            raw_headers.append([b'Content-Type', content_type.encode(self.charset)])

        return raw_headers

    async def __call__(self, scope, receive, send) -> None:
        await send(
            {
                'type': 'http.response.start',
                'status': self.status_code,
                'headers': self.raw_headers,
            }
        )
        await send(
            {
                'type': 'http.response.body',
                'body': self.body,
            }
        )
