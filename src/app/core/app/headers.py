from src.app.core.app.types import Scope


class Headers:
    encoding = 'utf-8'

    def __init__(self, scope: Scope) -> None:
        self._headers = list(scope['headers'])

    def items(self) -> list[tuple[str, str]]:
        return [(key.decode(self.encoding), value.decode(self.encoding)) for key, value in self._headers]

    def get(self, key: str, default: str | None = None) -> str | None:
        header_key = key.lower().encode(self.encoding)
        for key, value in self._headers:
            if key == header_key:
                return value.decode(self.encoding)
        return default

    def __contains__(self, key: str) -> bool:
        header_key = key.lower().encode(self.encoding)
        for key, _ in self._headers:
            if key == header_key:
                return True
        return False

    def __getitem__(self, key: str) -> str:
        header_key = key.lower().encode(self.encoding)
        for key, value in self._headers:
            if key == header_key:
                return value.decode(self.encoding)
        raise KeyError(key)

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({dict(self.items())})'
