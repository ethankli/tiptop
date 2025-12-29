import asyncio


class Participant:
    def __init__(self, host: str = "0.0.0.0", port: int = 6667):
        self.host = host
        self.port = port
