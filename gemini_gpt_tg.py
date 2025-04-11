from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import CommandStart
import asyncio

import google.generativeai as genai


def gemini(prompt):
    genai.configure(api_key="token")
    model = genai.GenerativeModel("gemini-2.0-flash")
    answer = model.generate_content(prompt)
    return answer.text

# Токен бота (получи у @BotFather)
BOT_TOKEN = "token"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
user_histories = dict()

# Обработка команды /start
@dp.message(CommandStart())
async def start_cmd(message: Message):
    global user_histories
    await message.answer("Привет! Я LoffGPT.\n\nСоздан @BorisloffDev для удобного использования Google Gemini из России без VPN.\n\nНапиши мне что-нибудь — и я отвечу!")
    user_histories[message.from_user.id] = 'История чата. Используй ее только для понимания контекста. Не ссылайся на нее, не повторяй старые сообщения. Отвечай только на текущее сообщение, которое находится выше истории'

# Обработка всех остальных сообщений
@dp.message()
async def handle_message(message: Message):
    user_id = message.from_user.id
    user_text = message.text
    global user_histories
    answer_by_gemini = gemini(user_text+user_histories[user_id])
    user_histories[user_id] += 'User: ' + user_text + 'Answer by AI: ' + answer_by_gemini
    await answer_by_gemini

# Запуск бота
async def main():
    await dp.start_polling(bot)


asyncio.run(main())
