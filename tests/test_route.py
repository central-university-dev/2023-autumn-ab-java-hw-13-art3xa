from unittest.mock import AsyncMock

import pytest

from src.app.core.app.response import Response
from src.app.core.app.route import Route


@pytest.mark.asyncio
async def test_route():
    async def endpoint(request):
        return Response('Hello, World!')

    route = Route(path="/test", endpoint=endpoint, methods=['GET'])
    scope = {"path": "/test", "method": "GET"}
    receive = AsyncMock()
    send = AsyncMock()
    await route.__call__(scope, receive, send)
    assert route.matches(scope)
    send.assert_called()
