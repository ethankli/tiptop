import asyncio

from util.logger import Logger
from util.datagram import Datagram
from util.datagram_iterator import DatagramIterator

from net.message_types import *


class MessageDirector:
    def __init__(self, host: str = "127.0.0.1", port: int = 6667):
        self.logger = Logger("MessageDirector")

        self.host = host
        self.port = port

        self.subscribers = {}

    async def start(self) -> asyncio.base_events.Server:
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        self.logger.info(f"MessageDirector started on {self.host}:{self.port}")
        return server

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(4096)
        addr = writer.get_extra_info('peername')

        dg = Datagram(data)
        dgi = DatagramIterator(dg)

        msg_type = dgi.get_uint16()
        if msg_type == CONTROL_SET_CHANNEL:
            self.logger.info("Got message type CONTROL_SET_CHANNEL")
            self.handle_subscribe(dgi.get_uint64(), writer)

    def handle_subscribe(self, channel: int, writer: asyncio.StreamWriter):
        self.subscribers[channel] = writer
        self.logger.info(f"Registered new subscriber {writer.get_extra_info('peername')} for channel {channel}")

    def handle_unsubscribe(self, channel: int, writer: asyncio.StreamWriter):
        self.subscribers.pop(channel, None)
        self.logger.info(f"Unregistered subscriber {writer.get_extra_info('peername')} from channel {channel}")
