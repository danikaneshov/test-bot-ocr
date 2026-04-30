import asyncio
import base64
import io
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message
from groq import Groq

# --- НАСТРОЙКИ ---
# Твои ключи сохранены
BOT_TOKEN = "7777795241:AAHbw82y19ex_9_fMK550RLcBCPJP-vvwVU"
GROQ_API_KEY = "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"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
client = Groq(api_key=GROQ_API_KEY)

# Промпт для модели
SYSTEM_PROMPT = """
Ты — ассистент по учету продаж. Твоя задача — внимательно изучить фотографию (это может быть список от руки, экран монитора или чек).
Найди и посчитай количество упоминаний или количество проданных единиц для двух позиций:
1. "Дымный коктейль"
2. "Дымный коктейль 2"

Выдай ответ строго в формате:
Дымный коктейль: [количество]
Дымный коктейль 2: [количество]
Если позиций нет, пиши 0. Не пиши лишнего текста.
"""

def encode_image(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

@dp.message(F.photo)
async def handle_photo(message: Message):
    wait_msg = await message.answer("Анализирую фото, подождите...")
    
    # Скачиваем фото в память
    photo = message.photo[-1]
    file_info = await bot.get_file(photo.file_id)
    photo_bytes = await bot.download_file(file_info.file_path)
    
    # Превращаем в base64
    base64_image = encode_image(photo_bytes.getvalue())

    try:
        # Отправляем в Groq с обновленной моделью
        completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-instant", 
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Сколько тут продаж этих позиций?"},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                        }
                    ]
                }
            ],
            temperature=0.1, # Низкая температура для точности
        )
        
        result = completion.choices[0].message.content
        await wait_msg.edit_text(f"Результаты анализа:\n\n{result}")
    
    except Exception as e:
        await wait_msg.edit_text(f"Произошла ошибка при обработке: {e}")

@dp.message()
async def start_info(message: Message):
    await message.answer("Пришли мне фото отчета или списка продаж, и я посчитаю 'Дымные коктейли'.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
