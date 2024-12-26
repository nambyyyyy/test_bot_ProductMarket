from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)

keyboard_personal_account = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Покупки')],
               [KeyboardButton(text='Приведи друга')],
               [KeyboardButton(text='Информация ▶️')],
               [KeyboardButton(text='◀️ Назад')]],
    resize_keyboard=True
)

async def add_button_purchas_info(text, number):
    return InlineKeyboardMarkup(
            inline_keyboard = [[InlineKeyboardButton(text=text,
            callback_data=f'purchase_{number}_{text}')]]
    )

keyboard_inform_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Обратная связь')],
               [KeyboardButton(text='Баланс')],
               [KeyboardButton(text='◀️ Назад')]],
    resize_keyboard=True
)