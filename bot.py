import asyncio

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

API_TOKEN = "8771446004:AAH7w6wp-H07iruHAkQua7vbs82v43oydFU"

bot = Bot(token=API_TOKEN)
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


@dp.message()
async def handle_buttons(message: types.Message):
    text = message.text or ""

    if "ПОДДЕРЖКА" in text:
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

    elif "БЫСТРЫЙ ЗАКАЗ" in text:
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

    else:
        # Кнопка каталога сама открывает Mini App, поэтому тут просто подсказка
        await message.answer("Чтобы начать, нажмите одну из кнопок ниже.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
