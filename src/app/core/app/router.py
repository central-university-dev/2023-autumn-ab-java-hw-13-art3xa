from src.app.core.app.response import Response
from src.app.core.app.route import Route


class Router:
    def __init__(self, routes: list[Route] = None) -> None:
        self.routes = routes or []

    async def __call__(self, scope, receive, send) -> None:
        scope['router'] = self
        for route in self.routes:
            match, child_scope = route.matches(scope)
            if match:
                scope.update(child_scope)
                await route.endpoint(scope, receive, send)
                return
        await self.not_found(scope, receive, send)

    @staticmethod
    async def not_found(scope, receive, send) -> None:
        response = Response('Not Found', status_code=404, headers={'Content-Type': 'text/plain'})
        await response(scope, receive, send)
