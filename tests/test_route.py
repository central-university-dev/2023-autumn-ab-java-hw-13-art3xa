from unittest.mock import AsyncMock, MagicMock

import pytest

from src.app.core.app.response import Response
from src.app.core.app.route import Route, request_response


@pytest.mark.asyncio
async def test_route():
    async def endpoint(request):
        return Response('Hello, World!')

    route = Route(path='/test', endpoint=endpoint, methods=['GET'])
    scope = {'path': '/test', 'method': 'GET'}
    receive = AsyncMock()
    send = AsyncMock()
    await route.__call__(scope, receive, send)
    assert route.matches(scope)
    send.assert_called()


@pytest.mark.asyncio
async def test_request_response():
    async def endpoint(request):
        return Response('Hello, World!')

    wrapped_endpoint = request_response(endpoint)
    scope = {'path': '/test', 'method': 'GET'}
    receive = AsyncMock()
    send = AsyncMock()
    await wrapped_endpoint(scope, receive, send)
    send.assert_called()


@pytest.mark.asyncio
async def test_route_wrong():
    async def endpoint(request):
        return Response('Hello, World!')

    route = Route(path='/test', endpoint=endpoint, methods=['GET'])
    scope = {'path': '/test', 'method': 'GET'}
    receive = AsyncMock()
    send = AsyncMock()
    await route.__call__(scope, receive, send)
    assert route.matches(scope)[0]
    send.assert_called()

    scope = {'path': '/wrong', 'method': 'GET'}
    assert not route.matches(scope)[0]

    scope = {'path': '/test', 'method': 'POST'}
    assert not route.matches(scope)[0]


def test_route_matches():
    mock_convertor = MagicMock()
    mock_convertor.convert.return_value = "converted_value"

    route = Route(path='/test/{param}', endpoint=MagicMock(), methods=['GET'])
    route.param_convertors = {"param": mock_convertor}
    scope = {'path': '/test/value', 'method': 'GET'}
    match, child_scope = route.matches(scope)

    mock_convertor.convert.assert_called_once_with('value')
    assert child_scope['path_params'] == {"param": "converted_value"}
