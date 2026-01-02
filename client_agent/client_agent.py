import asyncio
import time

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
        self.next_client_id = 1

    async def start(self) -> asyncio.base_events.Server:
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        self.logger.info(f"ClientAgent started on {self.host}:{self.port}")
        await self.participant.connect()
        self.participant.subscribe(self.ca_channel)
        self.logger.info(f"ClientAgent connected to MessageDirector at {self.participant.host}:{self.participant.port}")
        return server

    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(4096)
        addr = writer.get_extra_info('peername')

        dg = Datagram(data)
        dgi = DatagramIterator(dg)
        
        self.logger.info(f"Received {dg.get_data()!r} from {addr!r}")
        msg_type = dgi.get_uint16()
        self.logger.info(f"Received message type: {msg_type}")
        if msg_type == CLIENT_HEARTBEAT:
            self.logger.info("Got message type CLIENT_HEARTBEAT")
            # TODO - handle heartbeat using a watchdog timer
        elif msg_type == CLIENT_LOGIN:
            self.handle_client_login(dgi, writer)
        
    def handle_client_login(self, dgi: DatagramIterator, writer: asyncio.StreamWriter):
        self.logger.info("Got message type CLIENT_LOGIN")
        dc_hash = dgi.get_uint32()
        server_version = dgi.get_string()
        self.logger.info(f"Got DC hash: {dc_hash}, server version: {server_version}")
        
        # assign a channel for this client
        client_channel = CLIENT_CHANNEL_BASE + self.next_client_id
        self.next_client_id += 1
        # register the client with the ClientAgent
        self.register_client(client_channel, writer)
        # subscribe the client to the MessageDirector
        self.participant.subscribe(client_channel)

        # TODO - verify DC hash and server version, compare against expected values
        resp = Datagram()
        resp.add_uint16(CLIENT_LOGIN_RESP)
        resp.add_uint8(0)  # returnCode
        resp.add_uint32(1) # accountCode
        resp.add_string("") # errorString
        resp.add_string("dev") # userName
        resp.add_uint8(1) # canChat
        resp.add_uint32(time.time_ns() // 1_000_000_000) # sec
        resp.add_uint32((time.time_ns() % 1_000_000_000) // 1_000) # usec
        resp.add_string("YES") # whitelistEnabled
        asyncio.create_task(self.route_message(resp, client_channel))

    async def route_message(self, datagram: Datagram, channel: int):
        if channel in self.clients:
            writer = self.clients[channel]
            writer.write(datagram.get_data())
            await writer.drain()
        self.logger.info(f"Routed message {datagram.get_data()!r} to client on channel {channel}")

    def register_client(self, channel: int, writer: asyncio.StreamWriter):
        self.clients[channel] = writer
        self.logger.info(f"Registered new client {writer.get_extra_info('peername')} for channel {channel}")

    def unregister_client(self, channel: int, writer: asyncio.StreamWriter):
        self.clients.pop(channel, None)
        self.logger.info(f"Unregistered client {writer.get_extra_info('peername')} from channel {channel}")
