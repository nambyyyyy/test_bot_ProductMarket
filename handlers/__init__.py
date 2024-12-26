from .enter_hendlers import router as enter_router
from .information_hendlers import router as information_router
from .menu_hendlers import router as menu_router
from .personal_account_handlers import router as account_router
from .reg_hendlers import router as reg_router
from .validation import (validation_name_and_surname, is_valid_date,
                        is_valid_password, generate_password,
                        generate_random_13_digit_number)

routers = [enter_router, information_router, menu_router, account_router, reg_router]

__all__ = [
    'routers',
    'validation_name_and_surname',
    'is_valid_date',
    'is_valid_password',
    'generate_password',
    'generate_random_13_digit_number'
]