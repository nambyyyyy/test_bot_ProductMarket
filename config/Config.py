from dataclasses import dataclass
from environs import Env
from aiogram.types import BotCommand
from aiogram import Bot

@dataclass
class TgBot: token: str


@dataclass
class Conf: tg_bot: TgBot


def load_config(path: str | None = None) -> Conf:

    env: Env = Env()
    env.read_env(path)

    return Conf(tg_bot=TgBot(token=env('BOT_TOKEN')))


async def set_main_menu(bot: Bot):

    main_menu_commands = [
        BotCommand(command='/menu',
        description='Главное меню')
    ]

    await bot.set_my_commands(main_menu_commands)