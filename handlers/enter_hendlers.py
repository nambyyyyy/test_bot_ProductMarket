from aiogram import F, Router
from aiogram.types import ReplyKeyboardRemove, Message
from aiogram.filters import StateFilter
from FSM import StateRegistration, StateEntry, StateMenu, default_state
from keyboard import keyboard_phone, keyboard_registarion, keyboard_main_menu
from database import checking_registration, DataBase, creating_purchase, LEXICON


router = Router()


@router.message(F.text=='Вход', StateFilter(default_state))
async def login_process(message: Message, state: StateEntry):
    await message.answer(LEXICON['Первичный вход'], reply_markup=keyboard_phone)
    await state.set_state(StateEntry.waiting_for_phone)



@router.message(F.text=='Вход', StateFilter(StateEntry.waiting_for_login))
async def login_process(message: Message, state: StateEntry):
    await message.answer(LEXICON['Вход после ввода номера'])
    await state.set_state(StateEntry.waiting_for_password)



@router.message(F.contact, StateFilter(StateEntry.waiting_for_phone))
async def number_verification(message: Message, state: StateEntry):

    contact_number = message.contact.phone_number
    result = await checking_registration(contact_number)
    await state.update_data(contact_number=contact_number)

    if result:
        await message.answer(LEXICON['Пароль'], reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateEntry.waiting_for_password)

    else:
        await message.answer(LEXICON['Нет регистрации'], reply_markup=keyboard_registarion)
        await state.set_state(StateRegistration.waiting_for_registration)


@router.message(F.text, StateFilter(StateEntry.waiting_for_password))
async def password_verification(message: Message, state: StateEntry):
    contact_number = message.contact.phone_number
    if message.text == DataBase[contact_number]['password']:

        data = await state.get_data()
        contact_number = data.get('contact_number')
        await creating_purchase(contact_number)
        await message.answer(LEXICON['menu'], reply_markup=keyboard_main_menu)
        await state.set_state(StateMenu.waiting_for_menu_access)
    else:
        await message.answer(LEXICON['Неверный пароль'])
