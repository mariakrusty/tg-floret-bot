import os
import asyncio

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    FSInputFile,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram import F

API_TOKEN = os.getenv("API_TOKEN", "8771446004:AAG1y0Po9QnbOwTIcR4dk6cr5XV0IvyViuw")
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET", "super_secret")  # любая строка

# URL Railway, который ты пришлёшь (без окончания /webhook)
RAILWAY_URL = os.getenv("RAILWAY_URL", "https://tg-floret-bot.up.railway.app")
WEBHOOK_PATH = f"/webhook/{WEBHOOK_SECRET}"
WEBHOOK_URL = RAILWAY_URL + WEBHOOK_PATH

# FastAPI-приложение
app = FastAPI()

# Сессия и объекты бота
session = AiohttpSession()
bot = Bot(token=API_TOKEN, session=session)
dp = Dispatcher()

# Mini App каталога
catalog_webapp = WebAppInfo(url="https://floret-msk.ru/")

# Нижние кнопки
kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(
                text="ОТКРЫТЬ КАТАЛОГ FLORET",
                web_app=catalog_webapp,
            )
        ],
        [KeyboardButton(text="💬 ПОДДЕРЖКА")],
        [KeyboardButton(text="⚡ БЫСТРЫЙ ЗАКАЗ")],
    ],
    resize_keyboard=True,
)

WELCOME_TEXT = (
    "Добро пожаловать! 🌸\n"
    "Вы в официальном телеграм-боте салона цветов Floret в Черёмушках.\n\n"
    "Здесь вы можете выбрать букет, композицию или подарок. "
    "Мы собираем их из свежих цветов и доставляем за 60 минут по району Черёмушки и соседним кварталам, "
    "а также в любой конец Москвы и ближнего Подмосковья.\n\n"
    "Заказ можно оформить самостоятельно через Mini App в боте, "
    "написать нашим менеджерам в Telegram: @floretsalon "
    "или позвонить по телефону 8-800-300-71-60.\n\n"
    "Поддержка по заказам ежедневно с 9:00 до 22:00.\n"
    "Зону покрытия доставки можно уточнить у менеджера по телефону +7 (926) 022-27-50."
)


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    photo = FSInputFile("floret_welcome.jpg")
    await message.answer_photo(
        photo=photo,
        caption=WELCOME_TEXT,
        reply_markup=kb,
    )


@dp.message(F.text.contains("ПОДДЕРЖКА"))
async def support_handler(message: types.Message):
    kb_support = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="ОТКРЫТЬ ЧАТ С МЕНЕДЖЕРОМ",
                    url="https://t.me/floretsalon",
                )
            ]
        ]
    )
    await message.answer(
        "Нажмите кнопку ниже, чтобы открыть чат с менеджером.",
        reply_markup=kb_support,
    )


@dp.message(F.text.contains("БЫСТРЫЙ ЗАКАЗ"))
async def fast_order_handler(message: types.Message):
    kb_fast = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="НАПИСАТЬ МЕНЕДЖЕРУ",
                    url="https://t.me/floretsalon",
                )
            ]
        ]
    )
    await message.answer(
        "Для быстрого заказа нажмите кнопку ниже и напишите, что хотите.",
        reply_markup=kb_fast,
    )


@dp.message()
async def fallback_handler(message: types.Message):
    await message.answer("Чтобы начать, нажмите одну из кнопок ниже.")


@app.on_event("startup")
async def on_startup():
    # Устанавливаем webhook при старте FastAPI
    await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)


@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    await session.close()


@app.post(WEBHOOK_PATH)
async def telegram_webhook(request: Request):
    # Получаем апдейт от Telegram и передаём его в Dispatcher
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return JSONResponse({"ok": True})


# Опциональный health-check
@app.get("/")
async def root():
    return {"status": "ok"}
