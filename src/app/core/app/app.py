from src.app.core.app.route import Route
from src.app.core.app.router import Router


class App:
    def __init__(self, routes: list[Route]):
        self.router = Router(routes)

    async def __call__(self, scope, receive, send):
        scope['app'] = self
        await self.router(scope, receive, send)
