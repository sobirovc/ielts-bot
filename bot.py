import asyncio
import logging
import os
import random
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Command
from flask import Flask
from threading import Thread

API_TOKEN = '8601041203:AAEmbpW2PvY-1iom5pQENfHeF2yf9-bRz00'

logging.basicConfig(level=logging.INFO)
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

QUIZ_DATA = [
    # --- GRAMMAR & TENSES ---
    {
        "question": "Choose the correct option: She ______ to the library yesterday.",
        "options": ["go", "went", "has gone", "going"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'went'. Chunki 'yesterday' iborasi o'tgan zamonni (Past Simple) bildiradi."
    },
    {
        "question": "If I ______ more time, I would learn another language.",
        "options": ["have", "had", "will have", "have had"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'had'. Bu 2-tur shartli gap (Second Conditional: If + Past Simple, would + verb)."
    },
    {
        "question": "By the time we arrived at the cinema, the movie ______.",
        "options": ["already started", "has already started", "had already started", "starts"],
        "correct_option_id": 2,
        "explanation": "To'g'ri javob: 'had already started'. O'tgan zamonda sodir bo'lgan voqeadan oldinroq yuz bergan ish-harakat uchun Past Perfect ishlatiladi."
    },
    {
        "question": "Neither my brother nor my parents ______ able to attend the event.",
        "options": ["was", "were", "is", "has been"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'were'. 'Neither... nor' birikmasida fe'l o'ziga eng yaqin turgan otdan ('parents' - ko'plik) kelib chiqib moslashadi."
    },
    {
        "question": "Hardly ______ when the telephone rang.",
        "options": ["I had arrived", "had I arrived", "I arrived", "did I arrive"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'had I arrived'. Gap 'Hardly' so'zi bilan boshlanganda inversiya (fe'l egadan oldinga o'tishi) sodir bo'ladi."
    },

    # --- VOCABULARY & SYNONYMS ---
    {
        "question": "IELTS Vocabulary: What is a synonym for 'Huge'?",
        "options": ["Tiny", "Enormous", "Slight", "Narrow"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'Enormous'. Ikkala so'z ham 'juda katta/ulkan' ma'nosini bildiradi."
    },
    {
        "question": "Choose the best synonym for the word 'DETRIMENTAL':",
        "options": ["Beneficial", "Harmful", "Essential", "Unimportant"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'Harmful'. 'Detrimental' so'zi 'zararli/ziyon keltiruvchi' degan ma'noni beradi."
    },
    {
        "question": "Select the antonym (opposite) of 'OBSOLETE':",
        "options": ["Outdated", "Modern", "Ancient", "Useless"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'Modern'. 'Obsolete' eskargan degani, uning qarama-qarshisi esa 'Modern' (zamonaviy)."
    },
    {
        "question": "What does the word 'AMBIGUOUS' mean?",
        "options": ["Clear and distinct", "Unclear or having double meaning", "Ambitious and hard-working", "Very dangerous"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'Unclear or having double meaning'. 'Ambiguous' — noaniq yoki ikkita ma'nosi bor tushuncha."
    },
    {
        "question": "Find the correct synonym for 'MITIGATE':",
        "options": ["Increase", "Reduce", "Ignore", "Destroy"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'Reduce'. 'Mitigate' — ta'sirini kamaytirmoq, yumshatmoq ma'nosida keladi."
    },

    # --- PREPOSITIONS & COLLOCATIONS ---
    {
        "question": "Choose the correct preposition: He is interested ______ learning English.",
        "options": ["on", "at", "in", "for"],
        "correct_option_id": 2,
        "explanation": "To'g'ri javob: 'in'. 'Interested' sifati har doim 'in' predlogi bilan ishlatiladi (interested in)."
    },
    {
        "question": "Despite ______ hard, he failed the final examination.",
        "options": ["he studied", "studying", "of studying", "he study"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'studying'. 'Despite' predlogidan keyin bevosita Fe'l+ing (gerund) yoki Ot keladi ('of' ishlatilmaydi)."
    },
    {
        "question": "She excels ______ solving complex mathematical problems.",
        "options": ["at", "in", "with", "on"],
        "correct_option_id": 0,
        "explanation": "To'g'ri javob: 'at'. 'Excel at something' — biror narsada juda usta/iqtidorli bo'lmoq iborasi."
    },
    {
        "question": "The government aims to curb pollution ______ implementing new policies.",
        "options": ["by", "with", "throughout", "for"],
        "correct_option_id": 0,
        "explanation": "To'g'ri javob: 'by'. Usul yoki vositani ko'rsatish uchun 'by + doing something' birikmasi qo'llaniladi."
    },
    {
        "question": "I am looking forward ______ you at the conference next week.",
        "options": ["to see", "to seeing", "for seeing", "see"],
        "correct_option_id": 1,
        "explanation": "To'g'ri javob: 'to seeing'. 'Look forward to' iborasidan keyin har doim Fe'l+ing (gerund) keladi."
    }
]

# Har qanday xabar yuborilganda tasodifiy savol yuborish
@dp.message()
async def send_quiz(message: types.Message):
    quiz = random.choice(QUIZ_DATA)
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
