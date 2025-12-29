import asyncio

from client_agent.client_agent import ClientAgent


async def main():
    client_agent = ClientAgent(host="127.0.0.1", port=7198)
    await client_agent.start()


if __name__ == "__main__":
    asyncio.run(main())
