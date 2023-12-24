import pytest

from src.app.core.app.convertors import CONVERTORS
from src.app.core.app.route import parse_path


def test_parse_path_no_params():
    path = "/test"
    regex, format, convertors = parse_path(path)
    assert regex.pattern == "^/test$"
    assert format == "/test"
    assert convertors == {}


def test_parse_path_one_param():
    path = "/test/{param:str}"
    regex, format, convertors = parse_path(path)
    assert regex.pattern == "^/test/(?P<param>[^/]+)$"
    assert format == "/test/{param}"
    assert convertors == {"param": CONVERTORS["str"]}


def test_parse_path_multiple_params():
    path = "/test/{param1:int}/{param2:str}"
    regex, format, convertors = parse_path(path)
    assert regex.pattern == "^/test/(?P<param1>[0-9]+)/(?P<param2>[^/]+)$"
    assert format == "/test/{param1}/{param2}"
    assert convertors == {"param1": CONVERTORS["int"], "param2": CONVERTORS["str"]}


@pytest.mark.parametrize("param_type,convertor",
                         [("str", CONVERTORS["str"]), ("int", CONVERTORS["int"]), ("uuid", CONVERTORS["uuid"]),
                          ("path", CONVERTORS["path"])])
def test_parse_path_supported_types(param_type, convertor):
    path = f"/test/{{param:{param_type}}}"
    regex, format, convertors = parse_path(path)
    assert regex.pattern == f"^/test/(?P<param>{convertor.regex})$"
    assert format == "/test/{param}"
    assert convertors == {"param": convertor}


def test_parse_path_unsupported_type():
    path = "/test/{param:unsupported}"
    with pytest.raises(AssertionError, match="Unknown path convertor 'unsupported'"):
        parse_path(path)
