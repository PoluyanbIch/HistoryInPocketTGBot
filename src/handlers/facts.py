from aiogram import types, Dispatcher
from utils.storage import get_random_fact
from keyboards.main_kb import main_menu


async def send_daily_fact(message: types.Message):
    fact = get_random_fact()
    tags = " ".join([f"#{tag}" for tag in fact.get("tags", [])])
    response = (
        f"📜 Исторический факт ({fact['category']}):\n"
        f"{tags}\n\n"
        f"{fact['content']}\n"
        f"Хотите ещё? Нажмите кнопку снова!"
    )
    await message.answer(response, reply_markup=main_menu())


def register_facts_handlers(dp: Dispatcher):
    dp.message.register(send_daily_fact, lambda msg: msg.text == "📜 Случайный факт")
