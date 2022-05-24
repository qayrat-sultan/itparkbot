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

main_menu_data = CallbackData('menu', 'action')


async def about_inline_kb(locale):
    confirm_lang = CallbackData('about', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("📝 Kursga yozilish",
                                           callback_data=confirm_lang.new(action="register")),
                types.InlineKeyboardButton("⬅️ Ortga",
                                           callback_data=main_menu_data.new(action="back")),
            ]
        ],
    )
    return inline_key


async def register_inline_kb(locale):
    confirm_lang = CallbackData('register', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🏢 IT Park Tashkent",
                                           callback_data=confirm_lang.new(action="tashkent"))
            ],
            [
                types.InlineKeyboardButton("🏢 IT Center Mirzo-Ulug'bek",
                                           callback_data=main_menu_data.new(action="mirzo")),
            ],
            [
                types.InlineKeyboardButton("🏢 IT Center Chilonzor",
                                           callback_data=confirm_lang.new(action="chilonzor"))
            ],
            [
                types.InlineKeyboardButton("🏢 IT Center Sergeli",
                                           callback_data=confirm_lang.new(action="sergeli"))
            ],
            [
                types.InlineKeyboardButton("🏢 IT Center Yakkasaroy",
                                           callback_data=confirm_lang.new(action="yakkasaroy"))
            ],
            [
                types.InlineKeyboardButton("🏢 IT Center Bektemir",
                                           callback_data=confirm_lang.new(action="bektemir"))
            ],
            [
                types.InlineKeyboardButton("⬅️ Ortga",
                                           callback_data=confirm_lang.new(action="back"))
            ]
        ],
    )
    return inline_key


async def menu_inline_kb(locale):
    confirm_lang = CallbackData('menu', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("ℹ️ Biz haqimizda",
                                           callback_data=confirm_lang.new(action="about")),
                types.InlineKeyboardButton("🖥 Bizning kurslar",
                                           callback_data=confirm_lang.new(action="courses")),
            ],
            [
                types.InlineKeyboardButton("📞 Kontaktlar",
                                           callback_data=confirm_lang.new(action="contacts")),
                types.InlineKeyboardButton("🏢 O'qub markazlar",
                                           callback_data=confirm_lang.new(action="centres")),
            ]
        ],
    )
    return inline_key