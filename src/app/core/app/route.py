from src.app.core.app.request import Request
from src.app.core.app.types import Receive, Scope, Send


def request_response(func):
    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive, send)
        response = await func(request)
        await response(scope, receive, send)

    return app


class Route:
    def __init__(self, path: str, endpoint) -> None:
        self.path = path
        self.endpoint = request_response(endpoint)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        await self.endpoint(scope, receive, send)

    def matches(self, scope) -> tuple[bool, Scope]:
        return self.path == scope['path']
