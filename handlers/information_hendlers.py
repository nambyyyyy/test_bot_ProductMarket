from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from FSM import StateInformation, StateAccount
from keyboard import (keyboard_feedback, keyboard_back,
                      keyboard_personal_account, keyboard_inform_menu,
                      keyboard_approval_card)
from database import is_card, LEXICON

router = Router()
quality = ['Отзыв на качество обслуживания', 'Общие вопросы', 'Неправильный баланс на карте', 'Ваши предложения и пожелания']


@router.message(F.text == 'Обратная связь', StateFilter(StateInformation.waiting_for_menu_information))
async def command_feedback(message: Message, state: StateInformation):
    await message.answer(text=LEXICON['Обратная связь'], reply_markup=keyboard_feedback)
    await state.set_state(StateInformation.waiting_for_feedback)


@router.message(F.text.in_(quality), StateFilter(StateInformation.waiting_for_feedback))
async def command_feedback(message: Message, state: StateInformation):
    await message.answer(text=LEXICON['Качество'], reply_markup=keyboard_back)
    await state.set_state(StateInformation.waiting_for_quality_information)


@router.message(F.text != '◀️ Назад', StateFilter(StateInformation.waiting_for_quality_information))
async def command_feedback(message: Message, state: StateInformation):
    await message.answer(text=LEXICON['Отзыв принят'], reply_markup=keyboard_back)
    await state.set_state(StateInformation.waiting_for_back)


@router.message(F.text == '◀️ Назад', StateFilter(StateInformation.waiting_for_back))
async def command_feedback(message: Message, state: StateInformation):
        await message.answer(text=LEXICON['Меню'], reply_markup=keyboard_feedback)
        await state.set_state(StateInformation.waiting_for_feedback)


@router.message(F.text == '◀️ Назад', StateFilter(StateInformation.waiting_for_quality_information))
async def command_feedback(message: Message, state: StateInformation):
    await message.answer(text=LEXICON['Меню'], reply_markup=keyboard_feedback)
    await state.set_state(StateInformation.waiting_for_feedback)


@router.message(F.text == '◀️ Назад', StateFilter(StateInformation.waiting_for_feedback))
async def command_feedback(message: Message, state: StateInformation):
    await message.answer(text=LEXICON['Меню'], reply_markup=keyboard_inform_menu)
    await state.set_state(StateInformation.waiting_for_menu_information)


@router.message(F.text == 'Баланс', StateFilter(StateInformation.waiting_for_menu_information))
async def command_feedback(message: Message, state: StateInformation):
    data = await state.get_data()
    contact_number = data.get('contact_number')
    card = await is_card(contact_number)

    if not card:
        await message.answer(LEXICON['Нет карты'], reply_markup=keyboard_approval_card)
    else:
        await message.answer(text='Ваши 💰\n'
                        f'Карта: {card["number"]}\n'
                        f'Баланс: {card["balans"]} бон.')


@router.message(F.text == '◀️ Назад', StateFilter(StateInformation.waiting_for_menu_information))
async def command_feedback(message: Message, state: StateInformation):
    await message.answer(text=LEXICON['Меню'], reply_markup=keyboard_personal_account)
    await state.set_state(StateAccount.waiting_for_menu_account)