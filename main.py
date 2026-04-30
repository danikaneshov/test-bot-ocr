import asyncio
import io
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
import google.generativeai as genai

# --- НАСТРОЙКИ ---
# Твои рабочие ключи
BOT_TOKEN = "7777795241:AAHbw82y19ex_9_fMK550RLcBCPJP-vvwVU"
GEMINI_API_KEY = "AIzaSyCA7f_bsapb8uLta8dmv2JbrRjLJy6d_3Y"

# Настройка Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=(
        "Ты — эксперт по учету продаж. Твоя задача: проанализировать изображение "
        "(отчет, чек или список) и найти количество продаж для двух позиций:\n"
        "1. 'Дымный коктейль'\n"
        "2. 'Дымный коктейль 2'\n\n"
        "Выдай ответ строго в этом формате:\n"
        "Дымный коктейль: [число]\n"
        "Дымный коктейль 2: [число]\n\n"
        "Если позиция не найдена, пиши 0. Никаких лишних пояснений не давай."
    )
)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(F.photo)
async def handle_photo(message: Message):
    wait_msg = await message.answer("Анализирую фото, секунду...")
    
    # Получаем фото в лучшем качестве
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_bytes = await bot.download_file(file_info.file_path)
    
    try:
        # Подготовка данных для Gemini
        image_parts = [
            {
                "mime_type": "image/jpeg",
                "data": photo_bytes.getvalue()
            }
        ]
        
        # Запрос к нейронке
        response = model.generate_content([
            "Посчитай количество продаж указанных позиций на этом фото.",
            image_parts[0]
        ])
        
        # Отправляем результат пользователю
        await wait_msg.edit_text(f"Результаты анализа:\n\n{response.text}")
    
    except Exception as e:
        await wait_msg.edit_text(f"Произошла ошибка: {e}")

@dp.message()
async def start_info(message: Message):
    await message.answer(
        "Привет! Скинь мне фото отчета, и я посчитаю продажи 'Дымных коктейлей'.\n"
        "Я понимаю даже рукописный текст или фото экрана."
    )

async def main():
    print("Бот запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот выключен")
