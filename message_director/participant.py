import asyncio

from util.logger import Logger
from net.message_types import *

from util.datagram import Datagram


class Participant:
    def __init__(self, host: str = "127.0.0.1", port: int = 6667):
        self.logger = Logger("Participant")

        self.host = host
        self.port = port

        self.reader = None
        self.writer = None
        self.lock = asyncio.Lock()

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)

    async def route_message(self, datagram: Datagram):
        if self.writer is None:
            self.logger.error("No connection established, cannot route message.")
            return
        async with self.lock:
            self.writer.write(datagram.get_data())
            await self.writer.drain()

    def subscribe(self, channel: int):
        dg = Datagram()
        dg.add_uint16(CONTROL_SET_CHANNEL)
        dg.add_uint64(channel)
        asyncio.create_task(self.route_message(dg))

    def unsubscribe(self, channel: int):
        dg = Datagram()
        dg.add_uint16(CONTROL_REMOVE_CHANNEL)
        dg.add_uint64(channel)
        asyncio.create_task(self.route_message(dg))
