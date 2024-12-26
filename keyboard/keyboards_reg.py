from aiogram.types import (KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup)


from database import city

keyboard_registarion = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Регистрация')]],
    resize_keyboard=True
)

keyboard_start = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Регистрация'), KeyboardButton(text='Вход')]],
    resize_keyboard=True
)

keyboard_entrance = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Вход')]],
    resize_keyboard=True
)

keyboard_phone = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Отправить номер телефона", request_contact=True)]],
    resize_keyboard=True
)

keyboard_read = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Читать')]],
    resize_keyboard=True
)

keyboard_consent = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Я соглашаюсь')]],
    resize_keyboard=True
)

keyboard_floor = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='👱‍♂️'), KeyboardButton(text='👱‍♀️')]],
    resize_keyboard=True
)

keyboard_city = InlineKeyboardMarkup(
    inline_keyboard=[[InlineKeyboardButton(text=cit, callback_data=f'city_{i}')] for i, cit in enumerate(city, 1)])

keyboard_password = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Создать пароль')]],
    resize_keyboard=True
)

keyboard_mailing = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text='Да'), KeyboardButton(text='Нет')]],
    resize_keyboard=True
)
