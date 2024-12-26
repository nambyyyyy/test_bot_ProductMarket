import asyncio
from config import Conf, load_config, set_main_menu
from handlers import routers
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode



async def main():

    config: Conf = load_config('.env')

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    for router in routers:
        dp.include_router(router)

    dp.startup.register(set_main_menu)


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())