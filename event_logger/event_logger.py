import asyncio

from util.logger import Logger
from util.datagram import Datagram
from util.datagram_iterator import DatagramIterator

from message_director.participant import Participant

from net.message_types import *
from net.channels import *

class EventLogger:
    def __init__(self, host: str = "127.0.0.1", port: int = 7197, participant: Participant = Participant(), el_channel: int = EVENT_LOGGER):
        self.logger = Logger("EventLogger")

        self.host = host
        self.port = port
        self.participant = participant
        self.el_channel = el_channel

    async def start(self) -> asyncio.base_events.Server:
        server = await asyncio.start_server(self.handle_connection, self.host, self.port)
        self.logger.info(f"EventLogger started on {self.host}:{self.port}")
        await self.participant.connect()
        self.participant.subscribe(self.el_channel)
        self.logger.info(f"EventLogger connected to MessageDirector at {self.participant.host}:{self.participant.port}")
        return server
    
    async def handle_connection(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        data = await reader.read(4096)
        addr = writer.get_extra_info('peername')

        dg = Datagram(data)
        dgi = DatagramIterator(dg)
        
        self.logger.info(f"Received {dg.get_data()!r} from {addr!r}")
        msg_type = dgi.get_uint16()
        self.logger.info(f"Received message type: {msg_type}")
