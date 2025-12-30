import asyncio

from util.logger import Logger
from message_director.participant import Participant
from util.datagram import Datagram
from util.datagram_iterator import DatagramIterator
from net.message_types import *


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
        addr = writer.get_extra_info('peername')

        dg = Datagram(data)
        dgi = DatagramIterator(dg)
        # Skip the first 2 bytes (message length)
        dgi.get_bytes(2)
        
        self.logger.info(f"Received {dg.get_data()!r} from {addr!r}")
        msg_type = dgi.get_uint16()
        if msg_type == CLIENT_LOGIN:
            self.handle_client_login(dgi, writer)
        
    def handle_client_login(self, dgi: DatagramIterator, writer: asyncio.StreamWriter):
        self.logger.info("Got message type CLIENT_LOGIN")
        dc_hash = dgi.get_uint32()
        server_version = dgi.get_string()
        self.logger.info(f"Got DC Hash: {dc_hash}, server version: {server_version}")
