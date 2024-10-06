import asyncio

from aiogram import Bot,Dispatcher
from handlers import router
from database.models import async_main

async def main():
    await async_main()
    bot = Bot(token='7453990109:AAFh0P9GP2Nbkq7DpE9yfVsA4cZ8K8XtV6U')
    dp=Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__== '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')