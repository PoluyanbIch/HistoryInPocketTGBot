from aiogram import types, Dispatcher
from aiogram.filters import Command
from keyboards.main_kb import main_menu


async def start(message: types.Message):
    await message.answer(
        "📖 Добро пожаловать в бота «История в кармане»!\nВыберите действие:",
        reply_markup=main_menu()
    )


def register_base_handlers(dp: Dispatcher):
    dp.message.register(start, Command("start"))
