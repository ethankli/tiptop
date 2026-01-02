import asyncio

from message_director.message_director import MessageDirector
from message_director.participant import Participant

from client_agent.client_agent import ClientAgent

from event_logger.event_logger import EventLogger


async def main():
    md = MessageDirector(host="127.0.0.1", port=6667)
    message_director = await md.start()

    ca_peer = Participant(host="127.0.0.1", port=6667)
    ca = ClientAgent(host="127.0.0.1", port=7198, participant=ca_peer)
    client_agent = await ca.start()

    el_peer = Participant(host="127.0.0.1", port=6667)
    el = EventLogger(host="127.0.0.1", port=7197, participant=el_peer)
    event_logger = await el.start()

    async with message_director, client_agent, event_logger:
        await asyncio.gather(
            message_director.serve_forever(),
            client_agent.serve_forever(),
            event_logger.serve_forever()
        )


if __name__ == "__main__":
    asyncio.run(main())
