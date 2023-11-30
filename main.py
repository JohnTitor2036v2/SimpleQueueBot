import logging
import asyncio

from instances_for_main import bot, dp
from app.handlers import router as router_handlers
from app.admin import router as router_admin
from app.database.models import async_main


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    await async_main()
    dp.include_router(router_handlers)
    dp.include_router(router_admin)
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
