import asyncio
import websockets
from pydantic_ai import Agent
from dotenv import load_dotenv
import os

load_dotenv()
os.makedirs("logs", exist_ok=True)

agent_instance = Agent(
    'google-gla:gemini-1.5-flash',
    system_prompt="""
        Ты опытный Python-разработчик. Проведи ревью кода по следующим пунктам:
        1. Ошибки или баги
        2. Предложения по улучшению
        3. Замечания по стилю
        4. Общая оценка
        Формат вывода:
        --- Ошибки ---
        ...
        --- Улучшения ---
        ...
        --- Стиль ---
        ...
        --- Оценка ---
        ...
        Будь кратким и понятным. Используй Markdown.
    """
)

async def async_review(code):
    return await agent_instance.run(code)

async def agent():
    async with websockets.connect("ws://localhost:8765") as ws:
        await ws.send("register:reviewer")
        while True:
            code = await ws.recv()
            print(f"[Reviewer] Получен код:\n{code}")

            feedback = await async_review(code)

            if len(feedback.output) > 1500:
                feedback_text = feedback.output[:1400] + "\n\n⚠️ Output truncated for brevity."
            else:
                feedback_text = feedback.output

            print(f"[Reviewer] Отзыв:\n{feedback_text}")
            await ws.send(f"send:user:{feedback_text}")

            with open("logs/reviewer.log", "a") as f:
                f.write(f"\n===== Новый код =====\n{code}\n\n===== Отзыв =====\n{feedback_text}\n\n")

asyncio.run(agent())
