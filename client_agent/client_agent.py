import asyncio

from util.logger import Logger
from message_director.participant import Participant
from util.datagram import Datagram


class ClientAgent:
    def __init__(self, host: str = "127.0.0.1", port: int = 7198, participant: Participant = Participant()):
        self.logger = Logger("ClientAgent")

        self.host = host
        self.port = port
        self.participant = participant

    async def start(self):
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        self.logger.info(f"ClientAgent started on {self.host}:{self.port}")
        async with server:
            await server.serve_forever()

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(4096)
        dg = Datagram(data)
        addr = writer.get_extra_info('peername')
        self.logger.info(f"Received {dg.get_data()!r} from {addr!r}")
