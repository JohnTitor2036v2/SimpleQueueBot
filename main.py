import logging
import asyncio

from instances_for_main import bot, dp
from app.handlers import router as router_handlers
from app.admin import router as router_admin
from app.database.models import async_main
from aiogram.utils.callback_answer import CallbackAnswerMiddleware


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    await async_main()
    dp.include_router(router_handlers)
    dp.include_router(router_admin)
    dp.callback_query.middleware(CallbackAnswerMiddleware())
    await bot.delete_webhook(True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
