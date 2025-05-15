from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from config import BOT_TOKEN
from handlers.base import register_base_handlers
from handlers.facts import register_facts_handlers
from handlers.quiz import register_quiz_handlers
from handlers.longread import register_longread_handlers
import asyncio


async def main():
    bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()

    # Регистрация обработчиков
    register_base_handlers(dp)
    register_longread_handlers(dp)
    register_facts_handlers(dp)
    register_quiz_handlers(dp)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
