from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📜 Случайный факт")],
            [KeyboardButton(text="🎲 Викторина")],
            [KeyboardButton(text="🏆 Рейтинг")]
        ],
        resize_keyboard=True
    )
