from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


kb = ReplyKeyboardMarkup(
    keyboard = [
        [KeyboardButton(text = "Регистрация")],
        [
            KeyboardButton(text = "ℹ️ Информация"),
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
        [InlineKeyboardButton(text = "Купить полезный брокколи", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Купить сочное яблоко", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Купить вкусное киви", callback_data = "product_buying")],
        [InlineKeyboardButton(text = "Купить спелый гранат", callback_data = "product_buying")]
    ]
)