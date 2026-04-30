import asyncio
import io
import google.generativeai as genai
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message

# --- НАСТРОЙКИ ---
BOT_TOKEN = "7777795241:AAHbw82y19ex_9_fMK550RLcBCPJP-vvwVU"
GEMINI_API_KEY = "AIzaSyCA7f_bsapb8uLta8dmv2JbrRjLJy6d_3Y"

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)

# Твое актуальное название модели
MODEL_NAME = "gemini-3.1-flash-live-preview"

model = genai.GenerativeModel(
    model_name=MODEL_NAME,
    system_instruction=(
        "Ты — эксперт по учету продаж. Твоя задача: проанализировать изображение и найти количество продаж:\n"
        "1. 'Дымный коктейль'\n"
        "2. 'Дымный коктейль 2'\n\n"
        "Выдай ответ строго в этом формате:\n"
        "Дымный коктейль: [число]\n"
        "Дымный коктейль 2: [число]\n\n"
        "Если позиция не найдена, пиши 0. Не добавляй лишних слов."
    )
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def handle_photo(message: Message):
    wait_msg = await message.answer("Анализирую фото через Gemini 3.1...")
    
    # Скачивание фото
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_bytes = await bot.download_file(file_info.file_path)
    
    try:
        # Формируем контент для модели
        image_data = {"mime_type": "image/jpeg", "data": photo_bytes.getvalue()}
        
        # Запрос к 3.1 Flash
        response = model.generate_content([
            "Сколько тут продаж этих позиций?",
            image_data
        ])
        
        await wait_msg.edit_text(f"Результаты анализа:\n\n{response.text}")
    
    except Exception as e:
        await wait_msg.edit_text(f"Произошла ошибка при анализе: {e}")

@dp.message()
async def start_info(message: Message):
    await message.answer("Пришли фото отчета, я посчитаю 'Дымные коктейли'.")

async def main():
    print(f"Бот запущен на модели {MODEL_NAME}")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
