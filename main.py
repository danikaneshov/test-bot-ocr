import google.generativeai as genai

genai.configure(api_key="AIzaSyCA7f_bsapb8uLta8dmv2JbrRjLJy6d_3Y")

print("Доступные модели с поддержкой генерации контента:")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(f"ID: {m.name}")
