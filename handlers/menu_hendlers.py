from aiogram import F, Router
from aiogram.types import FSInputFile, CallbackQuery, Message
from aiogram.filters import StateFilter
from FSM import StateMenu, StateInformation, state_for_the_menu_command
from keyboard import (keyboard_main_menu, keyboard_approval_card,
                                    keyboard_link_card)
from database import is_card, registration_card, LEXICON, Loyalty_Program




router = Router()

@router.message(F.text=='/menu', StateFilter(*state_for_the_menu_command))
async def command_menu_process(message: Message, state: StateMenu):
    await message.answer(LEXICON['Меню'], reply_markup=keyboard_main_menu)
    await state.set_state(StateMenu.waiting_for_menu_access)


@router.message(F.text=='Карта', StateFilter(StateMenu.waiting_for_menu_access))
async def command_card_process(message: Message, state: StateMenu):
    data = await state.get_data()
    contact_number = data.get('contact_number')
    card = await is_card(contact_number)

    if not card:
        await message.answer(LEXICON['Нет карты'], reply_markup=keyboard_approval_card)
    else:
        await message.answer_photo(
        photo=FSInputFile('photo_2024-12-07_09-19-54.jpg'),
        caption=f'Бонусная 💳\n'
        f'N {card["number"]}\n'
        f'Статус карты: {card["status"]}\n\n'
        f'Баланс: {card["balans"]} бон.',
        reply_markup=keyboard_link_card
    )



@router.callback_query(StateFilter(StateInformation.waiting_for_menu_information))
@router.callback_query(StateFilter(StateMenu.waiting_for_menu_access))
async def command_card_registration(callback_query: CallbackQuery, state: StateMenu):

    current_state = await state.get_state()

    if callback_query.data == 'of1':
        data = await state.get_data()
        contact_number = data.get('contact_number')

        await registration_card(contact_number)

        if current_state == 'StateMenu:waiting_for_menu_access':
            await callback_query.message.answer(text='Карта зарегистрирована 🤝\n'
                                    'Чтобы получить информацию о карте напишите слово Карта')
        else:
            await callback_query.message.answer(text='Карта зарегистрирована 🤝\n'
                                    'Чтобы получить информацию о балансе напишите слово Баланс')

    else:
        await callback_query.message.answer(text='Вы можете оформить карту в любое время ❤️')

    await callback_query.answer()



@router.message(F.text == 'Условия программы лояльности', StateFilter(StateMenu.waiting_for_menu_access))
async def command_loyalty_info(message: Message, state: StateMenu):
    await message.answer(text=Loyalty_Program)
    await message.answer(text='🤷‍♂️')
    await state.set_state(StateMenu.waiting_for_menu_access)
