from uuid import UUID

import pytest

from src.app.core.app.convertors import IntConvertor, PathConvertor, StrConvertor, UUIDConvertor


def test_str_convertor():
    convertor = StrConvertor()
    assert convertor.convert('test') == 'test'
    assert convertor.to_str('test') == 'test'


def test_int_convertor():
    convertor = IntConvertor()
    assert convertor.convert('123') == 123
    assert convertor.to_str(123) == '123'


def test_path_convertor():
    convertor = PathConvertor()
    assert convertor.convert('test/path') == 'test/path'
    assert convertor.to_str('test/path') == 'test/path'


def test_uuid_convertor():
    convertor = UUIDConvertor()
    uuid_str = '12345678-1234-5678-1234-567812345678'
    assert convertor.convert(uuid_str) == UUID(uuid_str)
    assert convertor.to_str(UUID(uuid_str)) == uuid_str
