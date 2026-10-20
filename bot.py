import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from flask import Flask
from threading import Thread

API_TOKEN = '8601041203:AAEmbpW2PvY-1iom5pQENfHeF2yf9-bRz00'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

QUIZ_DATA = [
    {
        "question": "Choose the correct option: She ______ to the library yesterday.",
        "options": ["go", "went", "has gone", "going"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'went'. Chunki 'yesterday' iborasi o'tgan zamonni (Past Simple) bildiradi."
    },
    {
        "question": "IELTS Vocabulary: What is a synonym for 'Huge'?",
        "options": ["Tiny", "Enormous", "Slight", "Narrow"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'Enormous'. Ikkala so'z ham 'juda katta/ulkan' ma'nosini bildiradi."
    },
    {
        "question": "Choose the correct preposition: He is interested ______ learning English.",
        "options": ["on", "at", "in", "for"],
        "correct_option_id": 2,
        "explanation": "To'g'ri javob: 'in'. 'Interested' sifati har doim 'in' predlogi bilan ishlatiladi (interested in)."
    }
]

@dp.message(CommandStart())
@dp.message(Command("test"))
async def send_quiz(message: types.Message):
    quiz = QUIZ_DATA[0]
    await bot.send_poll(
        chat_id=message.chat.id,
        question=quiz["question"],
        options=quiz["options"],
        type='quiz',
        correct_option_id=quiz["correct_option_id"],
        explanation=quiz["explanation"],
        is_anonymous=False
    )

app = Flask('')

@app.route('/')
def home():
    return "IELTS Bot is active and running 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

async def main():
    t = Thread(target=run_flask)
    t.start()
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
                              
