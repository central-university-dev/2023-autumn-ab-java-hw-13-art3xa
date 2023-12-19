from unittest.mock import AsyncMock

import pytest

from src.app.core.app.response import Response
from src.app.core.app.route import Route
from src.app.core.app.router import Router


@pytest.mark.asyncio
async def test_router():
    async def endpoint(request):
        return Response('Hello, World!')

    route = Route(path="/test", endpoint=endpoint)
    router = Router(routes=[route])
    scope = {"type": "http", "path": "/test"}
    receive = AsyncMock()
    send = AsyncMock()

    await router.__call__(scope, receive, send)

    send.assert_called()


@pytest.mark.asyncio
async def test_not_found():
    async def endpoint(request):
        """This endpoint should never be called."""

    route = Route(path="/test", endpoint=endpoint)
    router = Router(routes=[route])
    scope = {"type": "http", "path": "/not_found"}
    receive = AsyncMock()
    send = AsyncMock()

    await router.__call__(scope, receive, send)

    send.assert_called()
