import json
from typing import Any, AsyncGenerator  # noqa: UP035

from src.app.core.app.headers import Headers
from src.app.core.app.query_params import QueryParams
from src.app.core.app.types import Receive, Scope, Send


class ClientDisconnect(Exception):
    pass


class Request:
    def __init__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.scope = scope
        self._receive = receive
        self._send = send
        self._stream_is_over = False

    @property
    def path_params(self) -> dict[str, Any]:
        return self.scope.get("path_params", {})

    @property
    def headers(self) -> Headers:
        return Headers(self.scope)

    @property
    def query_params(self) -> QueryParams:
        return QueryParams(self.scope)

    @property
    def receive(self) -> Receive:
        return self._receive

    @property
    def method(self) -> str:
        return self.scope["method"]

    async def read_stream(self) -> AsyncGenerator[bytes, None]:
        while not self._stream_is_over:
            message = await self._receive()
            if message["type"] == "http.request":
                body = message.get('body', b'')
                more_body = message.get('more_body', False)
                if not more_body:
                    self._stream_is_over = True
                if body:
                    yield body
            elif message["type"] == "http.disconnect":
                raise ClientDisconnect()
        yield b''

    async def body(self) -> bytes:
        body_chunks = []
        async for body_chunk in self.read_stream():
            body_chunks.append(body_chunk)
        return b''.join(body_chunks)

    async def json(self) -> Any:
        body = await self.body()
        return json.loads(body)

    def __getitem__(self, key: str) -> Any:
        return self.scope[key]
