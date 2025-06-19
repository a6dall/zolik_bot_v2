from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def main_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="✅ Приду", callback_data="coming")
    builder.button(text="❌ Занят", callback_data="busy")
    builder.adjust(2)            # 2 кнопки в ряд
    return builder.as_markup()
