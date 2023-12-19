class Request:
    def __init__(self, scope, receive, send) -> None:
        self.scope = scope
        self.receive = receive
        self.send = send
