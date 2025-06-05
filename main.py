import asyncio
import websockets

async def user():
    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send("register:user")
        task = input("📝 Введите задачу для кода: ")
        await ws.send(f"send:langchain:{task}")
        review = await ws.recv()
        print(f"\n📋 Результат ревью:\n{review}")

asyncio.run(user())
