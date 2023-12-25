from urllib.parse import parse_qsl

from src.app.core.app.types import Scope


class QueryParams:
    encoding = 'utf-8'

    def __init__(self, scope: Scope) -> None:
        self._query_params = parse_qsl(scope['query_string'].decode(self.encoding), keep_blank_values=True)
        self._dict = dict(self._query_params)

    def items(self) -> list[tuple[str, str]]:
        return self._query_params

    def __contains__(self, key: str) -> bool:
        return key in self._dict

    def __getitem__(self, key: str) -> str:
        return self._dict[key]

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.items()})'
