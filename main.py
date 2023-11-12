import sys
import logging
import asyncio

from instances_for_main import bot, dp
from app.handlers import router
from app.database.models import async_main


async def main():
    await async_main()
    dp.include_router(router)
    await dp.start_polling(bot,  skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')
