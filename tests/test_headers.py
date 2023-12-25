import pytest

from src.app.core.app.headers import Headers


@pytest.fixture
def headers():
    scope = {'type': 'http', 'headers': [(b'content-type', b'text/html')]}
    return Headers(scope)


def test_items(headers):
    assert headers.items() == [('content-type', 'text/html')]


def test_contains(headers):
    assert 'content-type' in headers
    assert 'non-existent-header' not in headers


def test_getitem(headers):
    assert headers['content-type'] == 'text/html'
    with pytest.raises(KeyError):
        _ = headers['non-existent-header']


def test_repr(headers):
    assert repr(headers) == "Headers({'content-type': 'text/html'})"


def test_get(headers):
    assert headers.get('content-type') == 'text/html'
    assert headers.get('non-existent-header') is None
    assert headers.get('non-existent-header', 'default') == 'default'
