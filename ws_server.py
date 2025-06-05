import asyncio
import websockets

clients = {}

async def handler(websocket):
    try:
        async for message in websocket:
            print(f"[Server] Received: {message}")
            if message.startswith("register:"):
                name = message.split(":", 1)[1]
                clients[name] = websocket
                print(f"[Server] {name} зарегистрирован.")
            elif message.startswith("send:"):
                parts = message.split(":", 2)
                if len(parts) < 3:
                    print("[Server] Неправильный формат сообщения.")
                    continue
                _, to, content = parts
                if to in clients:
                    await clients[to].send(content)
                    print(f"[Server] Передано → {to}")
                else:
                    print(f"[Server] Агент {to} не найден.")
    except Exception as e:
        print(f"[Server] Ошибка: {e}")


async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print("✅ WebSocket-сервер запущен на ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
