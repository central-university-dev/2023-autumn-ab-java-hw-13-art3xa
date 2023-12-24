from unittest.mock import AsyncMock

import pytest

from src.app.core.app.app import App
from src.app.core.app.response import Response
from src.app.core.app.route import Route


@pytest.mark.asyncio
async def test_app():
    async def endpoint(request):
        return Response('Hello, World!')

    route = Route(path="/test", endpoint=endpoint)
    app = App(routes=[route])
    scope = {"type": "http", "path": "/test", "method": "GET"}
    receive = AsyncMock()
    send = AsyncMock()

    await app.__call__(scope, receive, send)

    assert scope['app'] == app
    send.assert_called()
