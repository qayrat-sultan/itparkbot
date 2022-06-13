from aiogram import types
from aiogram.utils.callback_data import CallbackData

import configs
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


async def contacts_inline_kb(locale, message: types.Message):
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
    x = await configs.collpages.find_one({"slug": "contacts"})
    description = x['description_uz'] if locale == "uz" else x['description_ru']
    # await message.delete()
    # return await message.answer_photo(x['image'], parse_mode="HTML",
    #                                   reply_markup=inline_key, caption=description)
    return await message.edit_text(description, parse_mode="HTML",
                                   reply_markup=inline_key)


async def about_inline_kb(locale, message: types.Message):
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
    about_page = await configs.collpages.find_one({'slug': 'about'})
    description = about_page['description_uz'] if locale == "uz" else about_page['description_ru']
    return await message.answer_photo(about_page['image'], reply_markup=inline_key,
                                      caption=description)


async def reg_inline_kb(locale, data, message: types.Message):
    if data.get('courses') and data.get('register'):
        await message.answer(_("Iltimos, to'liq ismingizni kiriting", locale=locale),
                             reply_markup=await reply_back(locale))
        return await configs.SetRegister.fio.set()
    confirm_lang = CallbackData('reg', 'action')
    print("IM A DISCO DANCER", data)
    # TODO: after registration, user should be redirected to the main menu
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
    return await message.answer_photo(
        photo="AgACAgIAAxkDAAINjGKmwj2pWrA04nwUtGLclElONzKHAALLuTEbtgE5SYpQ3jzspBgsAQADAgADeAADJAQ",
        caption="CAPTION",
        reply_markup=inline_key,
    )


async def centers_text_dict_func(key, locale):
    centers_text_dict = {"tashkend": _("IT Park Tashkent", locale),
                         "mirzo": _("IT Center Mirzo-Ulug'bek", locale),
                         "chilonzor": _("IT Center Chilonzor", locale),
                         "sergeli": _("IT Center Sergeli", locale),
                         "yakkasaroy": _("IT Center Yakkasaroy", locale),
                         "bektemir": _("IT Center Bektemir", locale),
                         }
    return centers_text_dict[key]


async def register_inline_kb(locale, message: types.Message, data: dict = None):
    if data and data.get('courses'):
        print("URODINA")
        return await reg_inline_kb(locale, data, message)
    confirm_lang = CallbackData('register', 'action')
    print(data)
    centers = configs.collcenters.find({})  # noqa
    kb_course = []
    async for i in centers:
        kb_course.append(
            [
                types.InlineKeyboardButton(i["title_uz"] if locale == "uz" else i["title_ru"],
                                           callback_data=confirm_lang.new(action=i['slug']))
            ]
        )
    # Back button adding
    kb_course += [[
        types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
                                   callback_data=confirm_lang.new(action="back"))
    ]]
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=kb_course
    )
    x = await configs.collpages.find_one({"slug": "centers"})
    return await message.answer_photo(
        x['image'],
        reply_markup=inline_key,
        caption=x['description_uz'] if locale == "uz" else x['description_ru']
    )


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


async def courses_inline_kb(locale, message: types.Message):
    confirm_lang = CallbackData('courses', 'action')

    courses = configs.collcourses.find({})
    title = "title_uz" if locale == "uz" else "title_ru"
    kb_course = []
    async for i in courses:
        kb_course.append(
            [
                types.InlineKeyboardButton(i[title], callback_data=confirm_lang.new(action=i['slug']))
            ]
        )
    kb_course += [[
        types.InlineKeyboardButton(_("⬅️ Ortga", locale=locale),
                                   callback_data=confirm_lang.new(action="back"))
    ]]
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=kb_course
    )
    # course_photo = await configs.collcourses.find_one({'slug': 'courses'})
    x = await configs.collpages.find_one({'slug': 'courses'})
    return await message.answer_photo(
        x['image'],
        reply_markup=inline_key,
        caption=x['description_uz'] if locale == "uz" else x['description_ru']
    )


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


async def answer_report_inline(locale, user_id: str):
    confirm_sex = CallbackData('answer', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(_("Javob yozish", locale=locale),
                                           callback_data=confirm_sex.new(action=user_id)),
            ],
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
