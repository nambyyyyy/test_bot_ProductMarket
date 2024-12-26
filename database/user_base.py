from handlers.validation import generate_random_13_digit_number
import random

DataBase = {}
city = ['Калининград', 'Зеленоградск', 'Светлогорск', 'Пионерск']
random_date_and_time = ['01.01.2024 12:00', '14.02.2024 09:30',
                        '15.03.2024 18:45', '22.04.2024 11:15',
                        '30.05.2024 14:30', '05.06.2024 22:40',
                        '19.07.2024 07:10', '12.08.2024 16:20',
                        '23.09.2024 20:50', '30.10.2024 13:05']

random_magic = ['Юринат Продукт Калининград, Советский пр-т, д. 81, к. 4',
                'Юринат Продукт Калининград, Ленинский пр-т, д. 47, к. 15',
                'Юринат Продукт Светлогорск, ул. Лесная, д. 17, к. 1',
                'Юринат Продукт Зеленоградск, ул. Генерала-Карбышева, д. 1, к. 8',
                'Юринат Продукт Пионерск, ул. Солдатская, д. 78, к. 10']

supermarket_products = ["Молоко 850мл", "Хлеб 250г","Яйца 10шт", "Сыр 300г",
                        "Куриное филе 800г", "Яблоки 500г", "Помидоры 270г",
                        "Макароны 450г", "Шоколад 100г", "Кофе 280г"]


async def registration(phone):
    DataBase[phone] = {'authorization': False}

async def checking_registration(phone):
    return phone in DataBase and len(DataBase[phone]) == 8


async def authorization(phone):
    if not DataBase[phone]['authorization']:
        DataBase[phone]['authorization'] = True
        return True


async def log_out_account(phone):
    if DataBase[phone]['authorization']:
        DataBase[phone]['authorization'] = False
        return True


async def add_date(phone, key, data):
    DataBase[phone][key] = data

async def is_card(phone):
    if not 'card' in DataBase[phone]:
        return False
    return DataBase[phone]['card']

async def registration_card(phone):
    DataBase[phone]['card'] = {'number': generate_random_13_digit_number(),
                               'status': 'Активна ✅',
                               'balans': 250}


async def creating_purchase(phone):
    if 'purchases' not in DataBase[phone]:
        DataBase[phone]['purchases'] = []

    for _ in range(3):
        if random.choice([True, True, True, False]):
            purchase = DataBase[phone]['purchases']
            purchase.append({'Товары': []})
            discount = random.randint(1, 30)
            purchase_amount = 0

            for _ in range(random.randint(1, len(supermarket_products)+1)):

                product_price = float(f'{random.randint(100, 300)}.{random.randint(0, 99)}')
                amount_paid = round(product_price - ((discount / 100) * product_price), 2)
                purchase_amount += product_price
                product = random.choice(supermarket_products)

                purchase[-1]['Товары'].append({f'\n- {product}\n': {
                        f'   Количество': 1,
                        f'   Цена': f'{product_price:.2f} ₽'.replace('.', ','),
                        f'   Цена со скидкой': f'{amount_paid:.2f} ₽'.replace('.', ','),
                        f'   Скидка %': f'{discount}\n'}})


            amount_paid = purchase_amount - ((discount / 100) * purchase_amount)

            purchase[-1].update({
            'Номер': random.randint(1, 100),
            'Дата': random.choice(random_date_and_time),
            'Магазин': random.choice(random_magic),
            'Сумма покупки': f"{purchase_amount:.2f}".replace('.', ','),
            'Скидка %': discount,
            'Сумма к оплате': f"{amount_paid:.2f}".replace('.', ','),
            'Операция': 'Продажа'
            })
