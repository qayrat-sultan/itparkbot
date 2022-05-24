from aiogram import types
from aiogram.utils.callback_data import CallbackData

from main import _


async def start_keyboard(locale):
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(_("One", locale=locale))],
            [types.KeyboardButton(_("Two", locale=locale))],
            [types.KeyboardButton(_('Three', locale=locale))],
        ],
        resize_keyboard=True,
    )
    return kb

async def start_inline_kb(locale):
    confirm_lang = CallbackData('lang', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🇺🇿 O'zbek tili",
                                           callback_data=confirm_lang.new(action="uz")),
                types.InlineKeyboardButton("🇷🇺 Русский язык",
                                           callback_data=confirm_lang.new(action="ru")),
            ]
        ],
    )
    return inline_key
