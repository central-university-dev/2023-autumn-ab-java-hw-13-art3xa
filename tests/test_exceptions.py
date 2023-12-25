from src.app.core.app.exceptions import HTTPException


def test_http_exception_init():
    exception = HTTPException('Not Found', 404)
    assert exception.status_code == 404
    assert exception.content == 'Not Found'
    assert exception.headers is None


def test_http_exception_str():
    exception = HTTPException('Not Found', 404)
    assert str(exception) == '404: Not Found'


def test_http_exception_repr():
    exception = HTTPException('Not Found', 404)
    assert repr(exception) == 'HTTPException(status_code=404, message=Not Found)'


def test_http_exception_init_no_message():
    exception = HTTPException(status_code=404)
    assert exception.status_code == 404
    assert exception.content == 'Not Found'
    assert exception.headers is None
