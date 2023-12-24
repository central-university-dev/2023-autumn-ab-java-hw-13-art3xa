import json

import pytest

from src.app.core.app.json_response import JSONResponse


@pytest.fixture
def json_response():
    content = {"key": "value"}
    return JSONResponse(content)


def test_init(json_response):
    assert json_response.status_code == 200
    assert json_response.raw_headers == [[b'Content-Length', b'15'], [b'Content-Type', b'application/json']]
    assert json_response.media_type == 'application/json'


def test_init_body(json_response):
    content = {"key": "value"}
    assert json_response.init_body(content) == json.dumps(content, ensure_ascii=False, allow_nan=False, indent=None,
                                                          separators=(',', ':')).encode(json_response.charset)
