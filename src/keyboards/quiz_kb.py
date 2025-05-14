from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def quiz_keyboard(options):
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=option)] for option in options],
        resize_keyboard=True,
        one_time_keyboard=True
    )
