
import pytest

from src.app.core.app.query_params import QueryParams


@pytest.fixture
def query_params():
    scope = {'query_string': b'key1=value1&key2=value2'}
    return QueryParams(scope)


def test_items(query_params):
    assert query_params.items() == [('key1', 'value1'), ('key2', 'value2')]


def test_contains(query_params):
    assert 'key1' in query_params
    assert 'non-existent-key' not in query_params


def test_getitem(query_params):
    assert query_params['key1'] == 'value1'
    with pytest.raises(KeyError):
        _ = query_params['non-existent-key']


def test_repr(query_params):
    assert repr(query_params) == "QueryParams([('key1', 'value1'), ('key2', 'value2')])"
