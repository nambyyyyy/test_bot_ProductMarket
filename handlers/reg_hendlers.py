from aiogram import F, Router
from aiogram.types import ReplyKeyboardRemove, CallbackQuery, Message
from aiogram.filters import CommandStart, StateFilter
from FSM import StateRegistration, StateEntry, StateMenu, default_state
from keyboard import (keyboard_start, keyboard_entrance,
                                keyboard_phone, keyboard_read,
                                keyboard_consent, keyboard_floor,
                                keyboard_city, keyboard_password,
                                keyboard_mailing, keyboard_main_menu)

from database import (registration, add_date, creating_purchase, LEXICON)

from .validation import (validation_name_and_surname, is_valid_date,
                                is_valid_password, generate_password)


router = Router()

@router.message(CommandStart(), StateFilter(default_state))
async def command_start_process(message: Message):
    await message.answer(LEXICON['/start'], reply_markup=keyboard_start)


@router.message(F.text=='Регистрация', StateFilter(default_state))
async def registration_process(message: Message, state: StateRegistration):
    await message.answer(LEXICON['Первичный вход'], reply_markup=keyboard_phone)
    await state.set_state(StateRegistration.waiting_for_phone)


@router.message(F.text=='Регистрация', StateFilter(StateRegistration.waiting_for_registration))
async def registration_process(message: Message, state: StateRegistration):
    await message.answer(LEXICON['Регистрация после ввода номера'], reply_markup=keyboard_read)
    await state.set_state(StateRegistration.waiting_for_reading)


@router.message(F.contact, StateFilter(StateRegistration.waiting_for_phone))
async def process_entry_phone(message: Message, state: StateRegistration):
    contact_number = message.contact.phone_number
    result = await registration(contact_number)
    await state.update_data(contact_number=contact_number)

    if result:
        await message.answer(LEXICON['Уже зарегистрирован'], reply_markup=keyboard_entrance)
        await state.set_state(StateEntry.waiting_for_login)

    else:
        await message.answer(LEXICON['Регистрация после ввода номера'], reply_markup=keyboard_read)
        await state.set_state(StateRegistration.waiting_for_reading)




@router.message(F.text=='Читать', StateFilter(StateRegistration.waiting_for_reading))
async def reading_process(message: Message, state: StateRegistration):
    await message.answer(LEXICON['Читать'], reply_markup=keyboard_consent)
    await state.set_state(StateRegistration.waiting_for_consent)



@router.message(F.text=='Я соглашаюсь', StateFilter(StateRegistration.waiting_for_consent))
async def consent_process(message: Message, state: StateRegistration):
    await message.answer(LEXICON['Ввод имени'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(StateRegistration.waiting_for_name)



@router.message(F.text, StateFilter(StateRegistration.waiting_for_name))
async def process_entering_name(message: Message, state: StateRegistration):
    if not validation_name_and_surname(message.text):
        await message.answer(LEXICON['Некорректное имя'])
    else:
        data = await state.get_data()
        contact_number = data.get('contact_number')
        await add_date(contact_number, 'name', message.text)

        await message.answer(LEXICON['Ввод фамилии'], reply_markup=ReplyKeyboardRemove())
        await state.set_state(StateRegistration.waiting_for_surname)



@router.message(F.text, StateFilter(StateRegistration.waiting_for_surname))
async def process_entering_surname(message: Message, state: StateRegistration):
    if not validation_name_and_surname(message.text):
        await message.answer(LEXICON['Некорректная фамилия'])
    else:
        data = await state.get_data()
        contact_number = data.get('contact_number')
        await add_date(contact_number, 'surname', message.text)

        await message.answer(LEXICON['Выбор пола'], reply_markup=keyboard_floor)
        await state.set_state(StateRegistration.waiting_for_floor)


@router.message(F.text.in_(['мужской', 'женский', '👱‍♂️', '👱‍♀️']), StateFilter(StateRegistration.waiting_for_floor))
async def process_choosing_gender(message: Message, state: StateRegistration):
    data = await state.get_data()
    contact_number = data.get('contact_number')
    await add_date(contact_number, 'floor', {'👱‍♂️': 'man', '👱‍♀️': 'woman'}[message.text])

    await message.answer(LEXICON['Ввод даты рождения'], reply_markup=ReplyKeyboardRemove())
    await state.set_state(StateRegistration.waiting_for_age)


@router.message(F.text, StateFilter(StateRegistration.waiting_for_age))
async def process_choosing_city(message: Message, state: StateRegistration):
    result: bool = is_valid_date(message.text)
    if not result:
        await message.answer(LEXICON['Некорректная дата рождения'])
    else:
        if result < 13:
            await message.answer(LEXICON['Меньше 13 лет'])
            await state.set_state(default_state)
        else:
            data = await state.get_data()
            contact_number = data.get('contact_number')

            await add_date(contact_number, 'age', message.text)
            await state.set_state(StateRegistration.waiting_for_city)
            await message.answer(LEXICON['Выбор города'], reply_markup=keyboard_city)



@router.callback_query(StateFilter(StateRegistration.waiting_for_city))
async def process_creating_password(callback: CallbackQuery, state: StateRegistration):
    data = await state.get_data()
    contact_number = data.get('contact_number')
    await add_date(contact_number, 'city', callback.data)

    await callback.message.answer(LEXICON['Создание пароля'], reply_markup=keyboard_password)
    await callback.answer()
    await state.set_state(StateRegistration.waiting_for_password_registration)


@router.message(F.text=='Создать пароль', StateFilter(StateRegistration.waiting_for_password_registration))
async def password_approval(message: Message, state: StateRegistration):
    user_password = generate_password()
    await message.answer(f'Пароль сгенерирован: {user_password}')
    await message.answer(LEXICON['Пароль создан'], reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    contact_number = data.get('contact_number')
    await add_date(contact_number, 'password', user_password)

    await message.answer(LEXICON['Согласие на рассылку'], reply_markup=keyboard_mailing)
    await state.set_state(StateRegistration.waiting_for_mailing)


@router.message(F.text, StateFilter(StateRegistration.waiting_for_password_registration))
async def process_choosing_city(message: Message, state: StateRegistration):
    if not is_valid_password(message.text):
        await message.answer(LEXICON['Неправильный пароль'])
    else:
        await message.answer(f'Пароль сгенерирован: {message.text}')
        await message.answer(LEXICON['Пароль создан'], reply_markup=ReplyKeyboardRemove())

        data = await state.get_data()
        contact_number = data.get('contact_number')
        await add_date(contact_number, 'password', message.text)

        await message.answer(LEXICON['Согласие на рассылку'], reply_markup=keyboard_mailing)
        await state.set_state(StateRegistration.waiting_for_mailing)


@router.message(F.text.lower().in_(['да', 'нет']), StateFilter(StateRegistration.waiting_for_mailing))
async def consent_confirmation_process(message: Message, state: StateRegistration):
    data = await state.get_data()
    contact_number = data.get('contact_number')
    await add_date(contact_number, 'mailing', {'да': True, 'нет': False}[message.text.lower()])
    await creating_purchase(contact_number)
    await add_date(contact_number, 'authorization', True)

    await message.answer(LEXICON['Регистрация прошла успешно'])
    await message.answer(LEXICON['menu'], reply_markup=keyboard_main_menu)
    await state.set_state(StateMenu.waiting_for_menu_access)
