import asyncio
import websockets
import json


async def main():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"cmd": "join", "room": "general"}))
        print(await ws.recv())

        await ws.send(json.dumps({"cmd": "msg", "text": "hello everyone"}))

        msg = await ws.recv()
        print(msg)


if __name__ == '__main__':
    asyncio.run(main())
