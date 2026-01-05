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

        # channel subscriptions: channel_id -> StreamWriter
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

        """
        internal message routing logic is handled differently than client messages
        https://www.youtube.com/watch?v=SzybRdxjYoA

        2 bytes (uint16): msg length (not used)
        1 byte (uint8): count of channels targeted for this message
        8 bytes (uint64): [] channels targeted
        8 bytes (uint64): sender channel
        remaining bytes: payload

        TODO - implement internal message handling logic
        """

        self.logger.info(f"Received {dg.get_data()!r} from {addr!r}")

        # first channel is the control message channel
        # the rest are target channels, including the sender channel
        channels = []
        channel_count = dgi.get_uint8()

        # retrieve target channels for this message
        for _ in range(channel_count):
            channel = dgi.get_uint64()
            channels.append(channel)
        
        if channel_count < 2:
            self.logger.info("No target channels specified, dropping message")
            return
        elif channel_count == 2 and channels[0] == CONTROL_MESSAGE:
            # message is for us, handle control message
            self.logger.info("Received control message")
            msg_type = dgi.get_uint16()
            if msg_type == CONTROL_SET_CHANNEL:
                # subscribe request!
                sender_channel = channels[1]
                self.handle_subscribe(sender_channel, writer)
                return
            elif msg_type == CONTROL_REMOVE_CHANNEL:
                # unsubscribe request!
                sender_channel = channels[1]
                self.handle_unsubscribe(sender_channel, writer)
                return

        # message is not for us, route to subscribers   
        # fetch all subscribers for the target channels
        subscribers = self.fetch_subscribers(channels)
        if not subscribers:
            self.logger.info("No subscribers for target channels, dropping message")
            return
        # create a new datagram with the remaining data    
        dg = Datagram(dgi.get_data())
        # send downstream to all subscribers
        for subscriber in subscribers:
            subscriber.write(dg.get_data())
            await subscriber.drain()

    async def route_message(self, datagram: Datagram, channels: list[int]):
        # send the datagram to all subscribers on the given channels
        for channel in channels:
            if channel in self.subscribers:
                writer = self.subscribers[channel]
                writer.write(datagram.get_bytes())
                await writer.drain()

    def handle_subscribe(self, channel: int, writer: asyncio.StreamWriter):
        # register the writer for this channel
        self.subscribers[channel] = writer
        self.logger.info(f"Registered new subscriber {writer.get_extra_info('peername')} for channel {channel}")

    def handle_unsubscribe(self, channel: int, writer: asyncio.StreamWriter):
        # unregister the writer for this channel
        self.subscribers.pop(channel, None)
        self.logger.info(f"Unregistered subscriber {writer.get_extra_info('peername')} from channel {channel}")

    def fetch_subscribers(self, channels: list[int]) -> list[asyncio.StreamWriter]:
        # get all writers subscribed to the given channels
        writers = []
        for channel in channels:
            if channel in self.subscribers:
                writers.append(self.subscribers[channel])
        return writers
