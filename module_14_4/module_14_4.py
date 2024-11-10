from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from Marat_1.module_13.lectures_13.api_tg_bot import api_bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import logging
from crud_functions import *
from io import BytesIO

logging.basicConfig(level = logging.INFO)

bot = Bot(token = api_bot)
dp = Dispatcher(bot, storage = MemoryStorage())

kb = ReplyKeyboardMarkup(
    keyboard = [
        [
            KeyboardButton(text = "Информация"),
            KeyboardButton(text = "Рассчитать")
        ],
        [KeyboardButton(text = "Купить")]
    ], resize_keyboard = True
)

inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Формулы расчёта", callback_data = "formulas")],
        [InlineKeyboardButton(text = "Упрощенный вариант", callback_data = "Simplified_version")],
        [InlineKeyboardButton(text = "Доработанный вариант", callback_data = "Modified_version")]
    ]
)

inline_kb_buy = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text = "Product1", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product2", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product3", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Product4", callback_data = "product_buying")]
    ]
)

@dp.message_handler(commands = ["start"])
async def start(message):
    with open("img/open.png", "rb") as img:
        await message.answer_photo(img, f"Приветствую, {message.from_user.username} ", reply_markup = kb)

@dp.message_handler(text = "Информация")
async def inform(message):
    await message.answer("Информация о боте:\n"
                         "Вычисление суточного потребления каллорий по формуле Миффлина-Сан Жеора"
                         "Упрощенный вариант и"
                         "Доработанный вариант:"
                         "учитывает степень физической активности человека")

@dp.message_handler(text = "Рассчитать")
async def main_menu(message):
    with open("img/squirrel.png", "rb") as img:
        await message.answer_photo(img, "Выберите опцию:", reply_markup = inline_kb)

@dp.message_handler(text = "Купить")
async def det_buying_list(message):
    for product in get_all_products():
        image = BytesIO(product[4])
        image.name = "image.png"
        await message.answer_photo(image, f"Название : {product[1]} | Описание : {product[2]} | Цена : {product[3]}")
    await message.answer("Выберите продукт для покупки: ", reply_markup = inline_kb_buy)

@dp.callback_query_handler(text = "product_buying")
async def send_confirm_message(call):
    with open("img/rabbit.png", "rb") as img:
        await call.message.answer_photo(img, "Вы успешно приобрели продукт!")
        await call.answer()

@dp.callback_query_handler(text = "formulas")
async def get_formulas(call):
    await call.message.answer(
        "Упрощенный вариант:\n"
        "для мужчин: 10 x вес (кг) + 6.25 x рост(см) – 5 x возраст(г) + 5\n"
        "для женщин: 10 x вес (кг) + 6.25 x рост(см) – 5 x возраст(г) – 161\n"
        "Доработанный вариант\n"
        "для мужчин: (10 x вес (кг) + 6.25 x рост(см) – 5 x возраст(г) + 5) x A\n"
        "для женщин: (10 x вес (кг) + 6.25 x рост(см) – 5 x возраст(г) – 161) x A\n")
    await call.answer()

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()
    gender = State()
    option = State()

@dp.callback_query_handler(text = "Modified_version")
async def set_option(call):
    await call.message.answer("Оцените вашу активность (введите соответствующее значение):\n"
                         "Минимальная активность - 1.2\n"
                         "Слабая активность - 1.375\n"
                         "Средняя активность - 1.55\n"
                         "Высокая активность - 1.725\n"
                         "Экстра-активность - 1.9")
    await UserState.option.set()
    await call.answer()

@dp.message_handler(state = UserState.option)
async def set_age(message, state):
    await state.update_data(option = message.text)
    await message.answer("Введите свой возраст:", )
    await UserState.age.set()

@dp.callback_query_handler(text = "Simplified_version")
async def age(call):
    await call.message.answer("Введите свой возраст:")
    await UserState.age.set()
    await call.answer()

@dp.message_handler(state = UserState.age)
async def set_growth(message, state):
    await state.update_data(age = message.text)
    await message.answer("Введите свой рост (в см.):")
    await UserState.growth.set()

@dp.message_handler(state = UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth = message.text)
    await message.answer("Введите свой вес (в кг.):")
    await UserState.weight.set()

@dp.message_handler(state = UserState.weight)
async def set_gender(message, state):
    await state.update_data(weight = message.text)
    await message.answer("Введите свой пол (М , Ж):")
    await UserState.gender.set()

@dp.message_handler(state = UserState.gender)
async def send_calories(message, state):
    await state.update_data(gender = message.text)
    data = await state.get_data()
    print(data)
    try:
        if data['gender'] == 'М':
            calor = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) + 5
        elif data['gender'] == 'Ж':
            calor = 10 * float(data['weight']) + 6.25 * float(data['growth']) - 5 * float(data['age']) - 161
    except (ValueError, UnboundLocalError):
        await message.answer("Введены не корректные данные")
    try:
        if data.get("option") is None:
            await message.answer(f'Ваша норма калорий в сутки: {round(calor)}')
        else:
            await message.answer(f'Ваша норма калорий в сутки: {round(calor * float(data["option"]))}')
    except (ValueError, UnboundLocalError):
        await message.answer("Введены не корректные данные")
    await state.finish()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

    connection.commit()
    connection.close()

"""
 1. Упрощенный вариант формулы Миффлина-Сан Жеора:

для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;
для женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161.
2. Доработанный вариант формулы Миффлина-Сан Жеора, в отличие от упрощенного дает более точную информацию
    и учитывает степень физической активности человека:

для мужчин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) + 5) x A;
для женщин: (10 x вес (кг) + 6.25 x рост (см) – 5 x возраст (г) – 161) x A.

A – это уровень активности человека, его различают обычно по пяти степеням физических нагрузок в сутки:

Минимальная активность: A = 1,2.
Слабая активность: A = 1,375.
Средняя активность: A = 1,55.
Высокая активность: A = 1,725.
Экстра-активность: A = 1,9 (под эту категорию обычно подпадают люди, занимающиеся, например, тяжелой атлетикой,
или другими силовыми видами спорта с ежедневными тренировками, а также те, кто выполняет тяжелую физическую работу).
"""
