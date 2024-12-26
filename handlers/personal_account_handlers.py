from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message, FSInputFile
from FSM import StateMenu, StateAccount, StateInformation
from keyboard import (keyboard_personal_account, keyboard_main_menu,
                    add_button_purchas_info, keyboard_inform_menu)
from database import DataBase, LEXICON



router = Router()

@router.message(F.text == 'Личный кабинет ▶️', StateFilter(StateMenu.waiting_for_menu_access))
@router.message(F.text == 'Личный кабинет ▶️', StateFilter(StateMenu.waiting_for_card_operations))
async def command_menu_process(message: Message, state: StateMenu):
    await message.answer(text=LEXICON['menu'], reply_markup=keyboard_personal_account)
    await state.set_state(StateAccount.waiting_for_menu_account)


@router.message(F.text == 'Покупки', StateFilter(StateAccount.waiting_for_menu_account))
async def command_purchase_history(message: Message, state: StateAccount):
    data = await state.get_data()
    contact_number = data.get('contact_number')
    purchases = DataBase[contact_number]['purchases']

    if not purchases:
        await message.answer(text=LEXICON['Нет покупок'])
    else:
        for purchas in purchases:

            await message.answer(
                             f"Номер: {purchas['Номер']}\n"
                             f"Дата: {purchas['Дата']}\n"
                             f"Магазин: {purchas['Магазин']}\n"
                             f"Сумма покупки: {purchas['Сумма покупки']} ₽\n"
                             f"Скидка %: {purchas['Скидка %']}\n"
                             f"Сумма к оплате: {purchas['Сумма к оплате']} ₽",
                             reply_markup=await add_button_purchas_info('Подробнее', purchas['Номер']))


@router.callback_query(F.data.startswith('purchase_'))
async def process_purchases_info(callback: CallbackQuery, state: StateAccount):
    purchase_number, text = callback.data.split("_")[1:]
    data = await state.get_data()
    contact_number = data.get('contact_number')
    result = ''

    for purchase_info in DataBase[contact_number]['purchases']:

        if str(purchase_info['Номер']) == purchase_number:

            if text == 'Подробнее':

                for dict_product in purchase_info['Товары']:
                    for product, value in dict_product.items():
                        result += product
                        for key, values in value.items():
                            result += f'{key}: {values}\n'

                await callback.message.edit_text(
                f"Номер: {purchase_info['Номер']}\n"
                f"Дата: {purchase_info['Дата']}\n"
                f"Магазин: {purchase_info['Магазин']}\n"
                f"Операция: {purchase_info['Операция']}\n"
                f"Товары: {result}"
                f"Сумма покупки: {purchase_info['Сумма покупки']} ₽\n"
                f"Скидка %: {purchase_info['Скидка %']}%\n"
                f"Сумма к оплате: {purchase_info['Сумма к оплате']} ₽",
                reply_markup=await add_button_purchas_info('Кратко', purchase_info['Номер']))

                break

            else:
                await callback.message.edit_text(
                f"Номер: {purchase_info['Номер']}\n"
                f"Дата: {purchase_info['Дата']}\n"
                f"Магазин: {purchase_info['Магазин']}\n"
                f"Сумма покупки: {purchase_info['Сумма покупки']} ₽\n"
                f"Скидка %: {purchase_info['Скидка %']}%\n"
                f"Сумма к оплате: {purchase_info['Сумма к оплате']} ₽",
                reply_markup=await add_button_purchas_info('Подробнее', purchase_info['Номер']))

                break

    await callback.answer()


@router.message(F.text == 'Приведи друга', StateFilter(StateAccount.waiting_for_menu_account))
async def command_bring_friend(message: Message, state: StateAccount):
    await message.answer_photo(
        photo=FSInputFile('photo_2024-12-10_21-02-01.jpg'),
        caption=f'Поделись этим QR-кодом с другом 😎\n\n'
                f'200 баллов вам будут начислены после регистрации и первой покупки вашего друга в одном из сети наших магазинов')


@router.message(F.text == 'Информация ▶️', StateFilter(StateAccount.waiting_for_menu_account))
async def command_menu_information(message: Message, state: StateAccount):
    await message.answer(text=LEXICON['menu'], reply_markup=keyboard_inform_menu)
    await state.set_state(StateInformation.waiting_for_menu_information)


@router.message(F.text == '◀️ Назад', StateFilter(StateAccount.waiting_for_menu_account))
async def command_menu_information(message: Message, state: StateAccount):
    await message.answer(text=LEXICON['menu'], reply_markup=keyboard_main_menu)
    await state.set_state(StateMenu.waiting_for_menu_access)
