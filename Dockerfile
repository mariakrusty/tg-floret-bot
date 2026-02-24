FROM python:3.11-slim

# Чтобы не буферизовал вывод
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
COPY bot.py .
COPY floret_welcome.jpg .

# Устанавливаем зависимости (aiogram 3, fastapi, uvicorn)
RUN pip install --no-cache-dir -r requirements.txt

# По желанию можно явно открыть порт (для локальных запусков)
EXPOSE 8000

# Запускаем FastAPI-приложение с учётом переменной PORT от Railway
CMD ["sh", "-c", "uvicorn bot:app --host 0.0.0.0 --port ${PORT:-8000}"]
