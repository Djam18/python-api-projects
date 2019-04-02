import asyncio
import websockets
import json

rooms = {}
clients = {}


async def handle(websocket, path):
    clients[websocket] = {'room': None, 'name': f'user_{id(websocket)}'}
    try:
        async for message in websocket:
            data = json.loads(message)
            cmd = data.get('cmd')

            if cmd == 'join':
                room = data.get('room', 'general')
                clients[websocket]['room'] = room
                if room not in rooms:
                    rooms[room] = set()
                rooms[room].add(websocket)
                await websocket.send(json.dumps({"type": "joined", "room": room}))

            elif cmd == 'leave':
                room = clients[websocket]['room']
                if room and room in rooms:
                    rooms[room].discard(websocket)
                clients[websocket]['room'] = None
                await websocket.send(json.dumps({"type": "left"}))

            elif cmd == 'msg':
                room = data.get('room') or clients[websocket]['room']
                text = data.get('text', '')
                if room and room in rooms:
                    msg = json.dumps({
                        "type": "message",
                        "room": room,
                        "from": clients[websocket]['name'],
                        "text": text
                    })
                    await asyncio.gather(
                        *[ws.send(msg) for ws in rooms[room] if ws != websocket]
                    )

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        room = clients[websocket]['room']
        if room and room in rooms:
            rooms[room].discard(websocket)
        del clients[websocket]


async def main():
    async with websockets.serve(handle, 'localhost', 8765):
        await asyncio.Future()


if __name__ == '__main__':
    asyncio.run(main())
