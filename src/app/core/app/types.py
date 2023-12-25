from typing import Any, Awaitable, Callable, MutableMapping  # noqa: UP035

Message = MutableMapping[str, Any]
Scope = Message
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
