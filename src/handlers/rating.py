from aiogram import types, Dispatcher
from src.utils.storage import load_data
from src.keyboards.main_kb import main_menu
import logging


async def show_rating(message: types.Message):
    try:
        data = load_data()
        logging.info(f"Loaded data: {data}")

        if not data.get("users"):
            await message.answer("📊 Рейтинг пока пуст!", reply_markup=main_menu())
            return

        sorted_users = sorted(
            data["users"].items(),
            key=lambda item: item[1].get("score", 0),
            reverse=True
        )

        rating_text = "🏆 Топ игроков:\n"
        for i, (user_id, user_data) in enumerate(sorted_users[:10], 1):
            username = user_data.get("username", f"Пользователь {user_id}")
            score = user_data.get("score", 0)
            rating_text += f"{i}. {username} — {score} очков\n"

        await message.answer(rating_text, reply_markup=main_menu())

    except Exception as e:
        logging.error(f"Error in show_rating: {e}", exc_info=True)
        await message.answer("⚠️ Произошла ошибка при загрузке рейтинга")


def register_rating_handlers(dp: Dispatcher):
    dp.message.register(show_rating, lambda msg: "Рейтинг" in msg.text)
