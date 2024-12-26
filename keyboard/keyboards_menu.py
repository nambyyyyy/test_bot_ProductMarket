from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)


keyboard_main_menu = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Карта')],
               [KeyboardButton(text='Личный кабинет ▶️')],
               [KeyboardButton(text='Условия программы лояльности')]],
    resize_keyboard=True
)

keyboard_approval_card = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Оформить 🤝', callback_data='of1')],
               [InlineKeyboardButton(text='Не требуется 🙅‍♂️', callback_data='no1')]]
)


keyboard_link_card = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text='Добавить в Wallet', url='https://www.apple.com/wallet/')],
               [InlineKeyboardButton(text='Мобильное приложение', url='https://y-market.ru/')]]
)
