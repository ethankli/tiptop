import asyncio

from util.logger import Logger
from util.datagram import Datagram
from util.datagram_iterator import DatagramIterator

from net.message_types import *
from net.channels import *

from message_director.participant import Participant


class ClientAgent:
    def __init__(self, host: str = "127.0.0.1", port: int = 7198, participant: Participant = Participant(), ca_channel: int = CLIENT_AGENT):
        self.logger = Logger("ClientAgent")

        self.host = host
        self.port = port
        self.participant = participant
        self.ca_channel = ca_channel
        
        self.clients = {}

    async def start(self) -> asyncio.base_events.Server:
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        self.logger.info(f"ClientAgent started on {self.host}:{self.port}")
        await self.participant.connect()
        self.logger.info(f"ClientAgent connected to MessageDirector at {self.participant.host}:{self.participant.port}")
        return server

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(4096)
        addr = writer.get_extra_info('peername')

        dg = Datagram(data)
        dgi = DatagramIterator(dg)
        
        self.logger.info(f"Received {dg.get_data()!r} from {addr!r}")
        msg_type = dgi.get_uint16()
        if msg_type == CLIENT_LOGIN:
            self.handle_client_login(dgi, writer)
        
    def handle_client_login(self, dgi: DatagramIterator, writer: asyncio.StreamWriter):
        self.logger.info("Got message type CLIENT_LOGIN")
        dc_hash = dgi.get_uint32()
        server_version = dgi.get_string()
        self.logger.info(f"Got DC Hash: {dc_hash}, server version: {server_version}")
        
        # assign a channel for this client
        client_channel = CLIENT_CHANNEL_BASE + (id(self) & 0xFFFFF)
        # register the client with the ClientAgent
        self.register_client(client_channel, writer)
        # subscribe the client to the MessageDirector
        self.participant.subscribe(client_channel)

    def register_client(self, channel: int, writer: asyncio.StreamWriter):
        self.clients[channel] = writer
        self.logger.info(f"Registered new client {writer.get_extra_info('peername')} for channel {channel}")

    def unregister_client(self, channel: int, writer: asyncio.StreamWriter):
        self.clients.pop(channel, None)
        self.logger.info(f"Unregistered client {writer.get_extra_info('peername')} from channel {channel}")
