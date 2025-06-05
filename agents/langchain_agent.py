from dotenv import load_dotenv
load_dotenv()

from langchain_openai import ChatOpenAI
import asyncio
import websockets

async def agent():
    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send("register:langchain")
        while True:
            task = await ws.recv()
            print(f"[LangChain] Получено задание: {task}")
            llm = ChatOpenAI(model="gpt-4", temperature=0)
            code = llm.invoke(f"Напиши Python-код: {task}")
            print(f"[LangChain] Код готов, отправка на ревью...")
            await ws.send(f"send:reviewer:{code}")

asyncio.run(agent())
