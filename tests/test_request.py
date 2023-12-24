from unittest.mock import AsyncMock

import pytest

from src.app.core.app.headers import Headers
from src.app.core.app.query_params import QueryParams
from src.app.core.app.request import Request


@pytest.mark.asyncio
async def test_request_body():
    scope = {'type': 'http', 'path': '/test', 'method': 'GET', 'headers': [], 'query_string': b''}
    receive = AsyncMock()
    send = AsyncMock()

    request = Request(scope, receive, send)

    assert request.method == 'GET'
    assert request.path_params == {}
    assert isinstance(request.headers, Headers)
    assert isinstance(request.query_params, QueryParams)

    receive.side_effect = [{'type': 'http.request', 'body': b'test', 'more_body': False}]
    body = await request.body()
    assert body == b'test'


@pytest.mark.asyncio
async def test_request_json_body():
    scope = {'type': 'http', 'path': '/test', 'method': 'GET', 'headers': [], 'query_string': b''}
    receive = AsyncMock()
    send = AsyncMock()

    request = Request(scope, receive, send)

    receive.side_effect = [{'type': 'http.request', 'body': b'{"key": "value"}', 'more_body': False}]
    json_body = await request.json()
    assert json_body == {'key': 'value'}


@pytest.mark.asyncio
async def test_request_getitem():
    scope = {'type': 'http', 'path': '/test', 'method': 'GET', 'headers': [], 'query_string': b''}
    receive = AsyncMock()
    send = AsyncMock()

    request = Request(scope, receive, send)

    assert request['type'] == 'http'
    assert request['path'] == '/test'
    assert request['method'] == 'GET'
    assert request['headers'] == []
    assert request['query_string'] == b''
    with pytest.raises(KeyError):
        _ = request['nonexistent']
