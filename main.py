import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BotBlocked, BotKicked, UserDeactivated

import configs
import kbs
import texts
from configs import MEDIA

BOT_TOKEN = configs.BOT_TOKEN

# Setup bot Dispatcher
bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MongoStorage(uri=configs.MONGO_URL)
dp = Dispatcher(bot, storage=storage)

# Setup i18n middleware
i18n = configs.Localization(configs.I18N_DOMAIN,
                            configs.LOCALES_DIR)
dp.middleware.setup(i18n)

# Alias for gettext method
_ = i18n.lazy_gettext


class SetReport(StatesGroup):
    report = State()


class SetState(StatesGroup):
    lang = State()


class SetRegister(StatesGroup):
    fio = State()
    sex = State()
    age = State()
    center = State()
    course = State()
    tel = State()


@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, locale, state: FSMContext):
    async with state.proxy() as data:
        data.clear()
    x = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await x.delete()
    if await configs.collusers.count_documents({"_id": message.from_user.id}) < 1:
        await message.answer(texts.start_text,
                             reply_markup=await kbs.start_inline_kb(locale),
                             parse_mode="HTML")  # required use bot.send_message!
    else:
        await message.answer(texts.menu_text,
                             reply_markup=await kbs.menu_inline_kb(locale))


@dp.message_handler(commands="setlang")
async def cmd_setlang(message: types.Message):
    confirm_lang = CallbackData('lang', 'action')
    inline_key = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("🇷🇺",
                                           callback_data=confirm_lang.new(action="ru")),
                types.InlineKeyboardButton("🇺🇿",
                                           callback_data=confirm_lang.new(action="uz")),
                types.InlineKeyboardButton("🇺🇸",
                                           callback_data=confirm_lang.new(action="en"))
            ]
        ],
    )
    await message.answer(_("Select this lang"), reply_markup=inline_key)


@dp.message_handler(commands='lang')
async def cmd_lang(message: types.Message, locale):
    # For setting custom lang you have to modify i18n middleware
    await message.reply(_('Your current language: <i>{language}</i>').format(language=locale))


@dp.message_handler(commands=["main"])
async def menu(message: types.Message, locale, state: FSMContext):
    await message.answer(texts.menu_text,
                         reply_markup=await kbs.menu_inline_kb(locale))


"""
@dp.message_handler(commands=['post'])
async def post(message: types.Message):
    data = {'type': 'text', 'text': 'text', 'entities': None}
    users = 390736292,
    await admin_commands.send_post_all_users(data, users, bot)"""


@dp.message_handler(commands="centers", state="*")
async def centers_menu(message: types.Message, locale, state: FSMContext):
    x = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await x.delete()
    await message.answer_photo(
        MEDIA.get('centers'),
        reply_markup=await kbs.register_inline_kb(locale),
        caption=texts.register_list_text
    )


@dp.message_handler(state=SetRegister.fio, content_types="text")
async def set_fio_process(message: types.Message, locale, state: FSMContext):
    if message.text == await texts.back_reply_button(locale):
        return await centers_menu(message, locale, state)
    for i in message.text.split():
        if not i.isalpha():
            return await message.answer(texts.error_answer_text)
    async with state.proxy() as data:
        data['fio'] = message.text
    await SetRegister.tel.set()
    await message.answer(texts.phone_add_text, reply_markup=await kbs.reply_back_phone(locale))


@dp.message_handler(state=SetRegister.tel, content_types=["text", "contact"])
async def set_fio_process(message: types.Message, locale, state: FSMContext):
    x = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await x.delete()
    if message.text == await texts.back_reply_button(locale):
        await message.answer(texts.fio_answer_text, reply_markup=await kbs.reply_back(locale))
        return await SetRegister.fio.set()
    async with state.proxy() as data:
        if message.contact:
            data['tel'] = str(message.contact.phone_number)
        else:
            return await message.answer(texts.phone_error_answer,
                                        reply_markup=await kbs.reply_back_phone(locale))
    await SetRegister.sex.set()
    await message.answer(texts.sex_answer_text, reply_markup=await kbs.sex_inline(locale))


@dp.callback_query_handler(lambda call: call.data.endswith('back_tel'), state="*")
async def back_to_tel_process(callback: types.CallbackQuery, locale):
    await callback.answer()
    await SetRegister.tel.set()
    await callback.message.delete()
    await callback.message.answer(texts.phone_add_text, reply_markup=await kbs.reply_back_phone(locale))


@dp.callback_query_handler(lambda call: call.data.startswith('sex'), state=SetRegister.sex)
async def set_sex_process(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data['sex'] = callback.data.split(":")[1]
    await SetRegister.age.set()
    await callback.message.delete()
    await callback.message.answer(texts.age_answer_text, reply_markup=await kbs.reply_back(locale))


@dp.message_handler(state=SetRegister.age, content_types="text")
async def set_fio_process(message: types.Message, locale, state: FSMContext):
    async with state.proxy() as data:
        if message.text == await texts.back_reply_button(locale):
            await message.answer(texts.sex_answer_text, reply_markup=await kbs.sex_inline(locale))
            return await SetRegister.sex.set()
        if message.text.isdigit():
            if not 7 < int(message.text) < 60:
                await message.answer(texts.error_age_answer)
                return await SetRegister.age.set()
            data['age'] = message.text
            await message.answer(texts.result_answer_text.  # noqa dubl
                                 format(fio=data.get('fio'),
                                        sex=data.get('sex'),
                                        age=data.get('age'),
                                        center=await kbs.centers_text_dict_func(data.get('register'), locale),
                                        course=await kbs.course_dict_func(data.get('courses'), locale),
                                        phone=data.get('tel')
                                        ),
                                 reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer(texts.error_answer_text, reply_markup=await kbs.reply_back(locale))
            return await SetRegister.age.set()
    confirm_button = CallbackData('confirm', 'action')
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(_("✅️ Tasdiqlash", locale=locale),
                                           callback_data=confirm_button.new(action="yes")),
            ],
            [
                types.InlineKeyboardButton(_("❌ Bekor qilish", locale=locale),
                                           callback_data=confirm_button.new(action="no"))
            ]
        ],
    )
    await message.answer(texts.accept_form, reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith('confirm'), state="*")
async def set_sex_process(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    async with state.proxy() as data:
        if callback.data.split(":")[1] == "yes":
            await callback.message.answer(texts.success_message_text)
            await bot.send_message(configs.GROUP_ID,
                                   texts.new_request_text.  # noqa dubl
                                   format(fio=data.get('fio'),
                                          sex=data.get('sex'),
                                          age=data.get('age'),
                                          center=await kbs.centers_text_dict_func(data.get('register'), locale),
                                          course=await kbs.course_dict_func(data.get('courses'), locale),
                                          phone=data.get('tel')
                                          ))
            await state.finish()
        else:
            await state.finish()
            return await back_menu(callback, locale, state)


@dp.callback_query_handler(lambda call: call.data.startswith('lang'), state="*")
async def language_set(callback: types.CallbackQuery, locale):
    await callback.answer()
    lang = callback.data.split(":")[1]
    if await configs.collusers.count_documents({"_id": callback.from_user.id}) < 1:
        await configs.collusers.insert_one({"_id": callback.from_user.id, "lang": lang})
    else:
        configs.collusers.update_one({"_id": int(callback.from_user.id)}, {
            "$set": {"lang": lang}})
    configs.LANG_STORAGE[callback.from_user.id] = lang

    # await callback.message.delete()
    await callback.message.edit_text(texts.menu_text, reply_markup=await kbs.menu_inline_kb(lang))


@dp.callback_query_handler(lambda call: call.data.endswith('lang'), state="*")
async def language_set(callback: types.CallbackQuery, locale):
    await callback.answer()
    # await callback.message.delete()
    await callback.message.edit_text(texts.start_text, reply_markup=await kbs.start_inline_kb(locale))
    # await callback.message.answer_photo(MEDIA['about'], reply_markup=await kbs.start_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("back"), state='*')
async def back_menu(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    async with state.proxy() as data:
        data.clear()
        await state.finish()
    await callback.message.delete()
    await callback.message.answer(texts.menu_text, reply_markup=await kbs.menu_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("menu"), state='*')
async def main_menu(callback: types.CallbackQuery, locale):
    await callback.answer()
    # await callback.message.delete()
    await callback.message.edit_text(texts.menu_text, reply_markup=await kbs.menu_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("register"), state='*')
async def register_func(callback: types.CallbackQuery, locale):
    await callback.answer()
    await SetRegister.center.set()
    await callback.message.delete()
    await callback.message.answer_photo(
        MEDIA.get('centers'),
        reply_markup=await kbs.register_inline_kb(locale),
        caption=texts.register_list_text
    )


@dp.callback_query_handler(lambda call: call.data.endswith("courses"), state='*')  # END WITH
async def register_func(callback: types.CallbackQuery, locale):
    await callback.answer()
    await SetRegister.course.set()
    await callback.message.delete()
    await callback.message.answer_photo(
        MEDIA.get('courses'),
        reply_markup=await kbs.courses_inline_kb(locale),
        caption=texts.courses_text
    )
    await SetRegister.course.set()


@dp.callback_query_handler(lambda call: call.data.endswith("contacts"), state='*')
async def register_func(callback: types.CallbackQuery, locale):
    await callback.answer()
    await callback.message.edit_text(texts.contact_text, parse_mode="HTML",
                                     reply_markup=await kbs.contacts_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("about"), state='*')
async def menu_func(callback: types.CallbackQuery, locale):
    await callback.answer()
    await callback.message.delete()
    # await callback.message.edit_text(await texts.about_text), reply_markup=await kbs.about_inline_kb(locale=locale))
    await callback.message.answer_photo(MEDIA['about'], reply_markup=await kbs.about_inline_kb(locale),
                                        caption=texts.about_text)


@dp.callback_query_handler(lambda call: call.data.endswith("reg"), state="*")
async def reg_couse_func(callback: types.CallbackQuery, locale):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(_("Iltimos, to'liq ismingizni kiriting", locale=locale),
                                  reply_markup=await kbs.reply_back(locale))
    await SetRegister.fio.set()


@dp.callback_query_handler(lambda call: call.data.startswith("answer"), state="*")
async def report_callback(callback: types.CallbackQuery, state: FSMContext, locale):
    await callback.answer()
    # await callback.message.delete()
    await callback.message.answer(_("Iltimos, o'z shikoyat/taklif'ingizni jo'nating", locale=locale),
                                  reply_markup=await kbs.reply_back(locale))
    async with state.proxy() as data:
        data['answer'] = callback.data.split(":")[1]
    await SetReport.report.set()


@dp.callback_query_handler(lambda call: call.data.endswith("report"), state="*")
async def report_callback(callback: types.CallbackQuery, locale):
    await callback.answer()
    # await callback.message.delete()
    await callback.message.answer(_("Iltimos, o'z shikoyat/taklif'ingizni jo'nating", locale=locale),
                                  reply_markup=await kbs.reply_back(locale))
    await SetReport.report.set()


@dp.message_handler(state=SetReport.report, content_types=['text'])
async def report_handler(message: types.Message, state: FSMContext, locale):
    async with state.proxy() as data:
        print(data)
        sended_user_id = int(data.get('answer')) if data.get('answer', None) else message.from_user.id
        # if answer to user message
        if message.from_user.id != message.chat.id:
            try:
                await bot.send_message(chat_id=sended_user_id,
                                       text=_("Sizning murojaatingizga javob xati keldi",
                                              locale=configs.LANG_STORAGE[sended_user_id]))
                await bot.send_message(chat_id=sended_user_id,
                                       text=message.text,
                                       entities=message.entities,
                                       reply_markup=await kbs.answer_report_inline(configs.LANG_STORAGE[sended_user_id],
                                                                                   str(message.from_user.id)))
                await message.answer("Yuborildi", reply_markup=types.ReplyKeyboardRemove())
            except (TypeError, BotBlocked, BotKicked,
                    UserDeactivated, Exception) as e:
                logging.warning("Error sending answer to: {} \n{}".format(sended_user_id, e))
                await message.answer(_("Ushbu foydalanuvchi botdan foydalanmaydi yoki telegram o'chirilgan"))
            return await state.finish()

        # if back button use
        if message.text == await texts.back_reply_button(locale):
            await message.answer(_("Bekor qilindi."), reply_markup=types.ReplyKeyboardRemove())
            await message.delete()
            return await state.finish()

        # success sending for group
        await bot.send_message(chat_id=configs.GROUP_ID,
                               text=message.text,
                               entities=message.entities,
                               reply_markup=await kbs.answer_report_inline(configs.LANG_STORAGE[sended_user_id],
                                                                           str(message.from_user.id)))
        await message.answer(_("Yuborildi"), reply_markup=types.ReplyKeyboardRemove())
        await state.finish()
    await menu(message, locale=locale, state=state)


@dp.edited_message_handler()
async def msg_handler(message: types.Message):
    logging.error("edited_message_handler", message)


@dp.my_chat_member_handler()
async def some_handler(my_chat_member: types.ChatMemberUpdated):
    # if start new profile or stop the bot
    logging.error("my_chat_member_handler", my_chat_member)


@dp.chat_member_handler()
async def some_handler(chat_member: types.ChatMemberUpdated):
    logging.error("chat_member_handler", chat_member)


@dp.message_handler(content_types=configs.all_content_types)
async def some_text(message: types.Message):
    await message.answer(_("Botni qayta yoqish uchun /start ni bosing."))


#
# @dp.errors_handler()
# async def some_error(baba, error):
#     logging.error("error", baba, error)


@dp.callback_query_handler(state="*")
async def some_callback(callback: types.CallbackQuery, state: FSMContext, locale):
    await callback.answer()
    print(callback.data, "@@@@@@@@@@@@@@@@@")
    courses = configs.collcourses.find({})
    c_dict = {}
    async for c in courses:
        print("@@@@@@@@@@@@@@@@@@@@@@@@", c)
        c_dict[c['slug']] = {'duration': c['duration'],
                             'price': c['price'],
                             'image': c['image'],
                             }
    centers = configs.collcenters.find({})
    center_dict = {}
    async for c in centers:
        print("@@@@@@@@@@@@@@@@@@@@@@@@", c)
        center_dict[c['slug']] = {'phone': c['phone'],
                                  'image': c['image'],
                                  }
    photo_dict = {
        "frontend": (c_dict['frontend']['image'], texts.web_text.format(**c_dict['frontend'])),
        "backend": (c_dict['backend']['image'], texts.backend_text.format(**c_dict['backend'])),
        "android": (c_dict['android']['image'], texts.android_text.format(**c_dict['android'])),
        "robots": (c_dict['robots']['image'], texts.robots_text.format(**c_dict['robots'])),
        "graphics": (c_dict['graphics']['image'], texts.graphics_text.format(**c_dict['graphics'])),
        "english": (c_dict['english']['image'], texts.english_text.format(**c_dict['english'])),
        "smm": (c_dict['smm']['image'], texts.smm_text.format(**c_dict['smm'])),
        "scratch": (c_dict['scratch']['image'], texts.scratch_text.format(**c_dict['scratch'])),

        "course": center_dict['courses']['image'],
        "yakkasaroy": (center_dict['yakkasaroy']['image'], texts.filial_yakkasaroy),
        "tashkent": (center_dict['tashkent']['image'], texts.filial_tashkent),
        "chilonzor": (center_dict['chilonzor']['image'], texts.filial_chilonzor),
        "mirzo": (center_dict['mirzo']['image'], texts.filial_mirzo),
        "sergeli": (center_dict['sergeli']['image'], texts.filial_sergeli),
        "bektemir": (center_dict['bektemir']['image'], texts.filial_bektemir),
    }

    print(photo_dict['frontend'], "$$$$$$$$$$$$$$$$$$$$$$$$")
    level_data, target_data = callback.data.split(":")
    async with state.proxy() as data:
        data[level_data] = target_data
        await callback.message.delete()
        if not data.get('courses') and not data.get('register'):
            return
        if not data.get('courses'):
            await callback.message.answer_photo(photo_dict[data.get('register')][0],
                                                reply_markup=await kbs.courses_inline_kb(locale),
                                                caption=photo_dict[data.get('register')][1])
        elif not data.get('register'):
            await callback.message.answer_photo(photo_dict['course'], reply_markup=await kbs.register_inline_kb(locale),
                                                caption=texts.register_list_text)
        else:
            await callback.message.answer_photo(photo=photo_dict[data['courses']][0],
                                                caption=photo_dict[data['courses']][1],
                                                reply_markup=await kbs.reg_inline_kb(locale),
                                                )


if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=configs.on_startup,
                           on_shutdown=configs.on_shutdown, skip_updates=True)
