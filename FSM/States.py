from aiogram.fsm.state import State, StatesGroup

class StateRegistration(StatesGroup):
    waiting_for_registration = State()
    waiting_for_phone = State()
    waiting_for_reading = State()
    waiting_for_consent = State()
    waiting_for_name = State()
    waiting_for_surname = State()
    waiting_for_floor = State()
    waiting_for_age = State()
    waiting_for_city = State()
    waiting_for_password_registration = State()
    waiting_for_mailing = State()
    waiting_for_login = State()


class StateEntry(StatesGroup):
    waiting_for_phone = State()
    waiting_for_password = State()
    waiting_for_login = State()


class StateMenu(StatesGroup):
    waiting_for_menu_access = State()
    waiting_for_card_operations = State()
    waiting_for_making_card = State()


class StateAccount(StatesGroup):
    waiting_for_menu_account = State()


class StateInformation(StatesGroup):
    waiting_for_menu_information = State()
    waiting_for_feedback = State()
    waiting_for_quality_information = State()
    waiting_for_back = State()
    waiting_card_registered = State()



state_for_the_menu_command = [
        StateMenu.waiting_for_menu_access.state,
        StateMenu.waiting_for_card_operations.state,
        StateMenu.waiting_for_making_card.state,
        StateAccount.waiting_for_menu_account.state,
        StateInformation.waiting_for_menu_information.state,
        StateInformation.waiting_for_feedback.state,
        StateInformation.waiting_for_quality_information.state,
        StateInformation.waiting_for_back.state,
        StateInformation.waiting_card_registered.state,
    ]
