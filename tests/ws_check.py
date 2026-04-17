import asyncio
import json

import websockets


WS_URL = "ws://127.0.0.1:8100/ws/room-1"
HTTP_POST_URL = "http://127.0.0.1:8100/rooms/room-1/messages"


async def receive_once(name: str, ws) -> None:
    msg = await asyncio.wait_for(ws.recv(), timeout=10)
    print(f"[{name}] got:", msg)


async def post_message() -> None:
    payload = "username=ws-check&text=hello+from+http"
    reader, writer = await asyncio.open_connection("127.0.0.1", 8100)
    req = (
        "POST /rooms/room-1/messages HTTP/1.1\r\n"
        "Host: 127.0.0.1:8100\r\n"
        "Content-Type: application/x-www-form-urlencoded\r\n"
        f"Content-Length: {len(payload)}\r\n"
        "Connection: close\r\n\r\n"
        f"{payload}"
    )
    writer.write(req.encode("utf-8"))
    await writer.drain()
    data = await reader.read(-1)
    writer.close()
    await writer.wait_closed()
    print("[http] response:", data.decode("utf-8", errors="ignore").split("\r\n\r\n", 1)[-1])


async def main() -> None:
    async with websockets.connect(WS_URL) as ws1, websockets.connect(WS_URL) as ws2:
        await post_message()
        await asyncio.gather(
            receive_once("ws1", ws1),
            receive_once("ws2", ws2),
        )


if __name__ == "__main__":
    asyncio.run(main())
