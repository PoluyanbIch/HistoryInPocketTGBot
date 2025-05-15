from aiogram import types, Dispatcher
from utils.storage import load_data, get_random_quiz, check_answer, save_data
from keyboards.quiz_kb import quiz_keyboard
from keyboards.main_kb import main_menu


async def start_quiz(message: types.Message):
    quiz = get_random_quiz()
    user_id = str(message.from_user.id)

    # Обновляем текущий вопрос пользователя
    data = load_data()
    if user_id not in data["users"]:
        data["users"][user_id] = {"username": message.from_user.username, "score": 0}

    data["users"][user_id]["current_quiz"] = quiz["id"]
    save_data(data)

    await message.answer(
        f"🎲 Вопрос:\n{quiz['question']}",
        reply_markup=quiz_keyboard(quiz['options'])
    )


async def handle_quiz_answer(message: types.Message):
    data = load_data()
    user_id = str(message.from_user.id)

    # Проверяем, есть ли активный вопрос у пользователя
    if user_id not in data["users"] or not data["users"][user_id]["current_quiz"]:
        await message.answer("❌ Сначала запустите викторину командой /quiz")
        return

    # Получаем текущий вопрос пользователя
    quiz_id = data["users"][user_id]["current_quiz"]
    quiz = next((q for q in data["quizzes"] if q["id"] == quiz_id), None)

    if not quiz:
        await message.answer("❌ Ошибка: вопрос не найден")
        return

    # Проверяем, что ответ есть среди вариантов
    if message.text not in quiz["options"]:
        await message.answer("⚠️ Выберите вариант из предложенных!")
        return

    # Проверяем правильность ответа
    if check_answer(message.from_user.id, message.text):
        data["users"][user_id]["current_quiz"] = None
        data["users"][user_id]["score"] += 10
        save_data(data)
        await message.answer(
            f"✅ Правильно! +10 очков\nТекущий счёт: {data['users'][user_id]['score']}\nДополнительный факт:\n{quiz['fact']}",
            reply_markup=main_menu()
        )
    else:
        data["users"][user_id]["current_quiz"] = None
        save_data(data)
        await message.answer(f"❌ Неверно! Правильный ответ: {quiz['correct']}", reply_markup=main_menu())


def register_quiz_handlers(dp: Dispatcher):
    dp.message.register(start_quiz, lambda msg: msg.text == "🎲 Викторина")

    # Динамическая регистрация обработчика для любых текстовых сообщений
    @dp.message()
    async def handle_all_messages(message: types.Message):
        data = load_data()
        user_id = str(message.from_user.id)

        # Если у пользователя есть активный вопрос - проверяем ответ
        if user_id in data["users"] and data["users"][user_id]["current_quiz"]:
            await handle_quiz_answer(message)
