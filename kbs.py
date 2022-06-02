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
            ],
            [
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
                types.InlineKeyboardButton(_("📤 Murojaat qoldirish", locale=locale),
                                           callback_data=confirm_lang.new(action="report")),
            ],
            [
                types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
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
                types.InlineKeyboardButton(_("📝 Kursga yozilish", locale=locale),
                                           callback_data=confirm_lang.new(action="register")),
            ],
            [
                types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
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
                types.InlineKeyboardButton(_("📝 Kursga yozilish", locale=locale),
                                           callback_data=confirm_lang.new(action="reg")),
            ],
            [
                types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
                                           callback_data=confirm_lang.new(action="back")),
            ]
        ],
    )
    return inline_key


async def centers_text_dict_func(key, locale):
    centers_text_dict = {"tashkend": _("IT Park Tashkent", locale),
                         "mirzo": _("IT Center Mirzo-Ulug'bek", locale),
                         "chilonzor": _("IT Center Chilonzor", locale),
                         "sergeli": _("IT Center Sergeli", locale),
                         "yakkasaroy": _("IT Center Yakkasaroy", locale),
                         "bektemir": _("IT Center Bektemir", locale),
                         }
    return centers_text_dict[key]


async def register_inline_kb(locale):
    confirm_lang = CallbackData('register', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(_("🏢 IT Park Tashkent", locale=locale),
                                           callback_data=confirm_lang.new(action="tashkent"))
            ],
            [
                types.InlineKeyboardButton(_("🏢 IT Center Mirzo-Ulug'bek", locale=locale),
                                           callback_data=confirm_lang.new(action="mirzo")),
            ],
            [
                types.InlineKeyboardButton(_("🏢 IT Center Chilonzor", locale=locale),
                                           callback_data=confirm_lang.new(action="chilonzor"))
            ],
            [
                types.InlineKeyboardButton(_("🏢 IT Center Sergeli", locale=locale),
                                           callback_data=confirm_lang.new(action="sergeli"))
            ],
            [
                types.InlineKeyboardButton(_("🏢 IT Center Yakkasaroy", locale=locale),
                                           callback_data=confirm_lang.new(action="yakkasaroy"))
            ],
            [
                types.InlineKeyboardButton(_("🏢 IT Center Bektemir", locale=locale),
                                           callback_data=confirm_lang.new(action="bektemir"))
            ],
            [
                types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
                                           callback_data=confirm_lang.new(action="back"))
            ]
        ],
    )
    return inline_key


async def course_dict_func(key, locale):
    course_dict = {
        "frontend": _("Web dasturlash (Frontend)", locale),
        "backend": _("Backend dasturlash", locale),
        "android": _("Android ilovalarni yaratish", locale),
        "robots": _("Mobil robototexnika", locale),
        "graphics": _("Grafika va web dizayn", locale),
        "english": _("IT-English", locale),
        "smm": _("SMM-mutaxassis", locale),
        "scratch": _("Scratch + IT English", locale),
    }
    return course_dict[key]


async def courses_inline_kb(locale):
    confirm_lang = CallbackData('courses', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(_("🖥 Web dasturlash (Frontend)", locale=locale),
                                           callback_data=confirm_lang.new(action="frontend"))
            ],
            [
                types.InlineKeyboardButton(_("💻 Backend dasturlash", locale=locale),
                                           callback_data=confirm_lang.new(action="backend")),
            ],
            [
                types.InlineKeyboardButton(_("📲 Android ilovalarni yaratish", locale=locale),
                                           callback_data=confirm_lang.new(action="android"))
            ],
            [
                types.InlineKeyboardButton(_("🤖 Mobil robototexnika", locale=locale),
                                           callback_data=confirm_lang.new(action="robots"))
            ],
            [
                types.InlineKeyboardButton(_("🏞 Grafika va web dizayn", locale=locale),
                                           callback_data=confirm_lang.new(action="graphics"))
            ],
            [
                types.InlineKeyboardButton(_("🇺🇸 IT-English", locale=locale),
                                           callback_data=confirm_lang.new(action="english"))
            ],
            [
                types.InlineKeyboardButton(_("👩‍💻 SMM-menejer", locale=locale),
                                           callback_data=confirm_lang.new(action="smm"))
            ],
            [
                types.InlineKeyboardButton(_("🧩 Scratch + IT English", locale=locale),
                                           callback_data=confirm_lang.new(action="scratch"))
            ],
            [
                types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
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
                types.InlineKeyboardButton(_("ℹ️ Biz haqimizda", locale=locale),
                                           callback_data=confirm_lang.new(action="about")),
                types.InlineKeyboardButton(_("🖥 Bizning kurslar", locale=locale),
                                           callback_data=confirm_lang.new(action="courses")),
            ],
            [
                types.InlineKeyboardButton(_("🏢 O'quv markazlar", locale=locale),
                                           callback_data=confirm_lang.new(action="register")),
                types.InlineKeyboardButton(_("📞 Kontaktlar", locale=locale),
                                           callback_data=confirm_lang.new(action="contacts")),
            ],
            [
                types.InlineKeyboardButton(_("🌐 Tilni alishtirish", locale=locale),
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
                types.InlineKeyboardButton(_("🙎🏻‍♂️ Erkak", locale=locale),
                                           callback_data=confirm_sex.new(action="erkak")),

                types.InlineKeyboardButton(_("🙎🏻‍♀️ Ayol", locale=locale),
                                           callback_data=confirm_sex.new(action="ayol")),
            ],
            [
                types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
                                           callback_data=confirm_sex.new(action="back_tel"))
            ]
        ],
    )
    return inline_key


async def reply_back(locale):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(await texts.back_reply_button(locale=locale))]
        ],
        resize_keyboard=True)
    return markup


async def reply_back_phone(locale):
    markup = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(await texts.phone_add_button(locale), request_contact=True)],
            [types.KeyboardButton(await texts.back_reply_button(locale))]
        ],
        resize_keyboard=True)
    return markup
