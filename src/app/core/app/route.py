import re

from src.app.core.app.convertors import CONVERTORS
from src.app.core.app.request import Request
from src.app.core.app.response import Response
from src.app.core.app.types import Receive, Scope, Send

PARAM_REGEX = re.compile("{([a-zA-Z_][a-zA-Z0-9_]*)(:[a-zA-Z_][a-zA-Z0-9_]*)?}")


def parse_path(path: str) -> tuple[re.Pattern, str, dict[str, str]]:
    path_regex = "^"
    path_format = ""
    param_convertors = {}
    last_pos = 0
    for match in PARAM_REGEX.finditer(path):
        param_name, convertor_type = match.groups("str")
        convertor_type = convertor_type.lstrip(":")
        assert (convertor_type in CONVERTORS), f"Unknown path convertor '{convertor_type}'"
        convertor = CONVERTORS[convertor_type]
        path_regex += re.escape(path[last_pos: match.start()])
        path_regex += f"(?P<{param_name}>{convertor.regex})"
        path_format += path[last_pos: match.start()]
        path_format += "{%s}" % param_name
        param_convertors[param_name] = convertor
        last_pos = match.end()

    path_regex += re.escape(path[last_pos:]) + "$"
    path_format += path[last_pos:]
    return re.compile(path_regex), path_format, param_convertors


def request_response(func):
    async def app(scope: Scope, receive: Receive, send: Send) -> None:
        request = Request(scope, receive, send)
        response = await func(request)
        await response(scope, receive, send)

    return app


class Route:
    def __init__(self, path: str, endpoint, *, methods: list[str] | None = None) -> None:
        assert path.startswith("/"), "Routed paths must start with '/'"
        self.path = path
        self.endpoint = request_response(endpoint)
        if methods is None:
            methods = ["GET"]
        self.methods = {method.upper() for method in methods}
        self.path_regex, self.path_format, self.param_convertors = parse_path(path)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        match, child_scope = self.matches(scope)
        if not match:
            response = Response("Not Found", status_code=404)
            await response(scope, receive, send)
            return
        scope.update(child_scope)
        await self.endpoint(scope, receive, send)

    def matches(self, scope) -> tuple[bool, Scope]:
        match = self.path_regex.match(scope["path"])
        if match is None:
            return False, {}
        matched_params = match.groupdict()
        for key, value in matched_params.items():
            convertor = self.param_convertors.get(key)
            if convertor is not None:
                matched_params[key] = convertor.convert(value)
        path_params = dict(scope.get('path_params', {}))
        path_params.update(matched_params)
        child_scope = {'endpoint': self.endpoint, 'path_params': path_params}
        if self.methods and scope['method'] in self.methods:
            return True, child_scope
        return False, {}
