from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.utils.callback_data import CallbackData

import configs
import texts
from main import _


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
    if x:
        description = x['description_uz'] if locale == "uz" else x['description_ru']
        # await message.delete()
        # return await message.answer_photo(x['image'], parse_mode="HTML",
        #                                   reply_markup=inline_key, caption=description)
        return await message.edit_text(description, parse_mode="HTML",
                                       reply_markup=inline_key)
    else:
        return await message.answer(texts.empty_contacts)


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
    if about_page:
        description = about_page['description_uz'] if locale == "uz" else about_page['description_ru']
        return await message.answer_photo(about_page['image'], reply_markup=inline_key,
                                          caption=description)
    else:
        return await message.answer(texts.empty_about_page)


async def reg_inline_kb(locale, message: types.Message):
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
    return await message.answer_photo(
        photo="AgACAgIAAxkDAAINjGKmwj2pWrA04nwUtGLclElONzKHAALLuTEbtgE5SYpQ3jzspBgsAQADAgADeAADJAQ",
        caption="CAPTION",
        reply_markup=inline_key,
    )


async def register_inline_kb(locale, message: types.Message):
    confirm_lang = CallbackData('register', 'action')
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
    if x:
        return await message.answer_photo(
            x['image'],
            reply_markup=inline_key,
            caption=x['description_uz'] if locale == "uz" else x['description_ru']
        )
    else:
        return await message.answer(texts.empty_centers)


async def courses_inline_kb(locale, message: types.Message):
    confirm_lang = CallbackData('courses', 'action')

    courses = configs.collcourses.find({})
    title = "title_uz" if locale == "uz" else "title_ru"
    kb_course = []
    async for i in courses:
        print("@@@@@@@@@", i)
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
    print("$$$$$$$$", x)
    if x:
        return await message.answer_photo(
            x['image'],
            reply_markup=inline_key,
            caption=x['description_uz'] if locale == "uz" else x['description_ru']
        )
    else:
        return await message.answer(texts.empty_courses)


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
