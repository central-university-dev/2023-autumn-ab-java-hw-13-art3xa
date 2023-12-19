from unittest.mock import AsyncMock

import pytest

from src.app.core.app.response import Response


@pytest.fixture(scope='function')
def response():
    response = Response(content="Hello, World!", status_code=200)
    return response


def test_init_body(response):
    assert response.init_body("Hello, World!") == b"Hello, World!"


def test_init_headers(response):
    assert response.init_headers({"Content-Type": "text/plain"}) == [[b'Content-Type', b'text/plain'],
                                                                     [b'Content-Length', b'13']]


def test_content_none():
    response = Response()
    assert response.body == b''


def test_content_bytes():
    response = Response(b'Hello, World!')
    assert response.body == b'Hello, World!'


def test_content_str():
    response = Response('Hello, World!')
    assert response.body == b'Hello, World!'


def test_content_type_in_headers():
    response = Response(headers={'Content-Type': 'text/plain'})
    assert response.raw_headers == [[b'Content-Type', b'text/plain']]


def test_content_type_in_headers_with_charset():
    response = Response(headers={'Content-Type': 'text/plain; charset=utf-8'})
    assert response.raw_headers == [[b'Content-Type', b'text/plain; charset=utf-8']]


@pytest.mark.asyncio
async def test_call(response):
    send = AsyncMock()
    await response.__call__({}, {}, send)
    send.assert_any_call({
        'type': 'http.response.start',
        'status': 200,
        'headers': [[b'Content-Length', b'13'], [b'Content-Type', b'text/plain; charset=utf-8']],
    })
    send.assert_any_call({
        'type': 'http.response.body',
        'body': b'Hello, World!',
    })
