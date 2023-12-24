from uuid import UUID


class StrConvertor:
    regex = '[^/]+'

    def convert(self, value: str) -> str:
        return str(value)

    def to_str(self, value: str) -> str:
        return str(value)


class IntConvertor:
    regex = '[0-9]+'

    def convert(self, value: str) -> int:
        return int(value)

    def to_str(self, value: int) -> str:
        value = int(value)
        return str(value)


class PathConvertor:
    regex = '.*'

    def convert(self, value: str) -> str:
        return str(value)

    def to_str(self, value: str) -> str:
        return str(value)


class UUIDConvertor:
    regex = '[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}'

    def convert(self, value: str) -> UUID:
        return UUID(value)

    def to_str(self, value: UUID) -> str:
        return str(value)


CONVERTORS = {
    'str': StrConvertor(),
    'int': IntConvertor(),
    'uuid': UUIDConvertor(),
    'path': PathConvertor(),
}
