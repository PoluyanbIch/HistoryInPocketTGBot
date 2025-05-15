from aiogram import types, Dispatcher
from utils.storage import get_random_story
from keyboards.main_kb import main_menu
import json
import random
from pathlib import Path

STORAGE_PATH = Path(__file__).parent.parent / "longreads.json"


async def send_longread(message: types.Message):
    story = get_random_story()

    response = (
        story["name"] + "\n" +
        story["story"]
    )
    await message.answer(response, reply_markup=main_menu())


def register_longread_handlers(dp: Dispatcher):
    dp.message.register(send_longread, lambda msg: msg.text == "📜 Случайная статья")
