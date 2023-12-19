from src.app.core.app.request import Request


def request_response(func):
    async def app(scope, receive, send):
        request = Request(scope, receive, send)
        response = await func(request)
        await response(scope, receive, send)

    return app


class Route:
    def __init__(self, path: str, endpoint) -> None:
        self.path = path
        self.endpoint = request_response(endpoint)

    async def __call__(self, scope, receive, send) -> None:
        await self.endpoint(scope, receive, send)

    def matches(self, scope) -> bool:
        return self.path == scope['path']
