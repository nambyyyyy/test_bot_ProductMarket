from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup)


keyboard_feedback = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Отзыв на качество обслуживания')],
               [KeyboardButton(text='Общие вопросы')],
               [KeyboardButton(text='Неправильный баланс на карте')],
               [KeyboardButton(text='Ваши предложения и пожелания')],
               [KeyboardButton(text='◀️ Назад')]],
    resize_keyboard=True
)

keyboard_back = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='◀️ Назад')]],
    resize_keyboard=True)
