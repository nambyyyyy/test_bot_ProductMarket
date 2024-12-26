from datetime import datetime
import string
import random

def validation_name_and_surname(name: str) -> bool:
    return 1 < len(name) < 30 and all(alf.isalpha() for alf in name)


def is_valid_date(date_string: str) -> bool:
    try:
        birth_date = datetime.strptime(date_string, '%d.%m.%Y')
        current_date = datetime.now()
        age = current_date.year - birth_date.year
        if (current_date.month < birth_date.month) or \
            (current_date.month == birth_date.month and current_date.day < birth_date.day):
            age -= 1

        return age

    except ValueError:
        return False

def is_valid_password(password):
    return len(password) >= 6


def generate_password():

    length = random.randint(6, 10)

    characters = string.ascii_letters + string.digits + '?!%#&'  # Большие и маленькие буквы, цифры и специальные символы

    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def generate_random_13_digit_number():
    first_digit = random.randint(1, 9)

    remaining_digits = [random.randint(0, 9) for _ in range(12)]

    random_number = str(first_digit) + ''.join(map(str, remaining_digits))

    return random_number


