from aiogram import types
from aiogram.utils.callback_data import CallbackData

import texts
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


async def contacts_inline_kb(locale):
    confirm_lang = CallbackData('contacts', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("📤 Murojaat qoldirish",
                                           callback_data=confirm_lang.new(action="report")),
            ],
            [
                types.InlineKeyboardButton("⬅️ Ortga",
                                           callback_data=confirm_lang.new(action="menu")),
            ]
        ],
    )
    return inline_key


async def about_inline_kb(locale):
    confirm_lang = CallbackData('about', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("📝 Kursga yozilish",
                                           callback_data=confirm_lang.new(action="register")),
                types.InlineKeyboardButton("⬅️ Ortga",
                                           callback_data=confirm_lang.new(action="back")),
            ]
        ],
    )
    return inline_key


async def reg_inline_kb(locale):
    confirm_lang = CallbackData('reg', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("📝 Kursga yozilish",
                                           callback_data=confirm_lang.new(action="reg")),
            ],
            [
                types.InlineKeyboardButton("⬅️ Ortga",
                                           callback_data=confirm_lang.new(action="back")),
            ]
        ],
    )
    return inline_key


centers_text_dict = {"tashkend": "IT Park Tashkent",
                     "mirzo": "IT Center Mirzo-Ulug'bek",
                     "chilonzor": "IT Center Chilonzor",
                     "sergeli": "IT Center Sergeli",
                     "yakkasaroy": "IT Center Yakkasaroy",
                     "bektemir": "IT Center Bektemir",
                     }


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
                                           callback_data=confirm_lang.new(action="mirzo")),
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


course_dict = {
    "frontend": "Web dasturlash (Frontend)",
    "backend": "Backend dasturlash",
    "android": "Android ilovalarni yaratish",
    "robots": "Mobil robototexnika",
    "graphics": "Grafika va web dizayn",
    "english": "IT-English",
    "smm": "SMM-mutaxassis",
    "scratch": "Scratch + IT English",
}


async def courses_inline_kb(locale):
    confirm_lang = CallbackData('courses', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🖥 Web dasturlash (Frontend)",
                                           callback_data=confirm_lang.new(action="frontend"))
            ],
            [
                types.InlineKeyboardButton("💻 Backend dasturlash",
                                           callback_data=confirm_lang.new(action="backend")),
            ],
            [
                types.InlineKeyboardButton("📲 Android ilovalarni yaratish",
                                           callback_data=confirm_lang.new(action="android"))
            ],
            [
                types.InlineKeyboardButton("🤖 Mobil robototexnika",
                                           callback_data=confirm_lang.new(action="robots"))
            ],
            [
                types.InlineKeyboardButton("🏞 Grafika va web dizayn",
                                           callback_data=confirm_lang.new(action="graphics"))
            ],
            [
                types.InlineKeyboardButton("🇺🇸 IT-English",
                                           callback_data=confirm_lang.new(action="english"))
            ],
            [
                types.InlineKeyboardButton("👩‍💻 SMM-menejer",
                                           callback_data=confirm_lang.new(action="smm"))
            ],
            [
                types.InlineKeyboardButton("🧩 Scratch + IT English",
                                           callback_data=confirm_lang.new(action="scratch"))
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
                types.InlineKeyboardButton(_("🖥 Bizning kurslar", locale=locale),
                                           callback_data=confirm_lang.new(action="courses")),
            ],
            [
                types.InlineKeyboardButton("📞 Kontaktlar",
                                           callback_data=confirm_lang.new(action="contacts")),
                types.InlineKeyboardButton("🏢 O'quv markazlar",
                                           callback_data=confirm_lang.new(action="register")),
            ],
            [
                types.InlineKeyboardButton("⬅️ Ortga",
                                           callback_data=confirm_lang.new(action="lang")),
            ]

        ],
    )
    return inline_key


async def sex_inline(locale):
    confirm_sex = CallbackData('sex', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🙎🏻‍♂️ Erkak",
                                           callback_data=confirm_sex.new(action="erkak")),

                types.InlineKeyboardButton("🙎🏻‍♀️ Ayol",
                                           callback_data=confirm_sex.new(action="ayol")),
            ],
            [
                types.InlineKeyboardButton("⬅️ Ortga",
                                           callback_data=confirm_sex.new(action="back_tel"))
            ]
        ],
    )
    return inline_key


async def reply_back(locale):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(_(texts.back_reply_button, locale=locale))]
        ],
        resize_keyboard=True)
    return markup


async def reply_back_phone(locale):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(_(texts.phone_add_button, locale=locale), request_contact=True)],
            [types.KeyboardButton(_(texts.back_reply_button, locale=locale))]
        ],
        resize_keyboard=True)
    return markup
