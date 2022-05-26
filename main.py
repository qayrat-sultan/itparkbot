from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

import configs
import handlers
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
        await message.answer(await texts.start_text(locale),
                             reply_markup=await kbs.start_inline_kb(locale),
                             parse_mode="HTML")  # required use bot.send_message!
    else:
        await message.answer(await texts.menu_text(locale=locale),
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
    # print(locale)
    # For setting custom lang you have to modify i18n middleware
    await message.reply(_('Your current language: <i>{language}</i>').format(language=locale))


@dp.message_handler(commands=["main"])
async def menu(message: types.Message):
    print("LOW", message)
    await handlers.menu_handler(message)

"""
@dp.message_handler(commands=['post'])
async def post(message: types.Message):
    data = {'type': 'text', 'text': 'text', 'entities': None}
    users = 390736292,
    await admin_commands.send_post_all_users(data, users, bot)"""


@dp.message_handler(commands=["report"])
async def report(message: types.Message):
    await SetReport.report.set()
    await message.answer("Bizga o'z takliflaringizni yuboring!")


@dp.message_handler(commands="centers", state="*")
async def centers_menu(message: types.Message, locale):
    x = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await x.delete()
    await message.answer_photo(
        MEDIA.get('centers'),
        reply_markup=await kbs.register_inline_kb(locale),
        caption=await texts.register_list_text(locale)
    )


@dp.message_handler(state=SetReport.report,
                    content_types=configs.all_content_types)
async def report_process(message: types.Message, state: FSMContext):
    await handlers.report_process_handler(message, state, bot)


@dp.message_handler(state=SetRegister.fio, content_types="text")
async def set_fio_process(message: types.Message, locale, state: FSMContext):
    if message.text == await texts.back_reply_button(locale):
        return await centers_menu(message, locale, state)
    if not message.text.isalpha():
        return await message.answer(await texts.error_answer_text(locale))
    async with state.proxy() as data:
        data['fio'] = message.text
    await SetRegister.tel.set()
    await message.answer(await texts.phone_add_text(locale), reply_markup=await kbs.reply_back_phone(locale))


@dp.message_handler(state=SetRegister.tel, content_types=["text", "contact"])
async def set_fio_process(message: types.Message, locale, state: FSMContext):
    x = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await x.delete()
    if message.text == await texts.back_reply_button(locale):
        await message.answer(await texts.fio_answer_text(locale), reply_markup=await kbs.reply_back(locale))
        return await SetRegister.fio.set()
    async with state.proxy() as data:
        if message.contact:
            data['tel'] = str(message.contact.phone_number)
        else:
            return await message.answer(await texts.phone_error_answer(locale),
                                        reply_markup=await kbs.reply_back_phone(locale))
    await SetRegister.sex.set()
    await message.answer(await texts.sex_answer_text(locale), reply_markup=await kbs.sex_inline(locale))


@dp.callback_query_handler(lambda call: call.data.endswith('back_tel'), state="*")
async def back_to_tel_process(callback: types.CallbackQuery, locale):
    await callback.answer()
    await SetRegister.tel.set()
    await callback.message.delete()
    print("BAKRBAKRBAKRBAKRBAKRBAKR")
    await callback.message.answer(await texts.phone_add_text(locale), reply_markup=await kbs.reply_back_phone(locale))


@dp.callback_query_handler(lambda call: call.data.startswith('sex'), state=SetRegister.sex)
async def set_sex_process(callback: types.CallbackQuery, locale, state: FSMContext):
    print("TUUUT")
    await callback.answer()
    async with state.proxy() as data:
        data['sex'] = callback.data.split(":")[1]
    await SetRegister.age.set()
    await callback.message.delete()
    await callback.message.answer(await texts.age_answer_text(locale), reply_markup=await kbs.reply_back(locale))


@dp.message_handler(state=SetRegister.age, content_types="text")
async def set_fio_process(message: types.Message, locale, state: FSMContext):
    async with state.proxy() as data:
        if message.text == await texts.back_reply_button(locale):
            await message.answer(await texts.sex_answer_text(locale), reply_markup=await kbs.sex_inline(locale))
            return await SetRegister.sex.set()
        if message.text.isdigit():
            if not 7 < int(message.text) < 60:
                await message.answer(await texts.error_age_answer(locale))
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
            print(data)
        else:
            await message.answer(await texts.error_answer_text(locale), reply_markup=await kbs.reply_back(locale))
            return await SetRegister.age.set()
    confirm_button = CallbackData('confirm', 'action')
    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton("✅️ Tasdiqlash",
                                           callback_data=confirm_button.new(action="yes")),
            ],
            [
                types.InlineKeyboardButton("❌ Bekor qilish",
                                           callback_data=confirm_button.new(action="no"))
            ]
        ],
    )
    await message.answer("Iltimos, yuqoridagi ma’lumotlarizni tekshiring va «Tasdiqlash» tugmasini bosing.",
                         reply_markup=markup)


@dp.callback_query_handler(lambda call: call.data.startswith('confirm'), state="*")
async def set_sex_process(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    async with state.proxy() as data:
        if callback.data.split(":")[1] == "yes":
            await callback.message.answer(await texts.success_message_text(locale))
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
    print("^^^^^^^^^^^^", callback.data)
    lang = callback.data.split(":")[1]
    configs.LANG_STORAGE[callback.from_user.id] = lang
    configs.collusers.update_one({"_id": int(callback.from_user.id)}, {
        "$set": {"lang": lang}})
    await callback.answer(_("Selected", locale=lang))
    # await callback.message.delete()
    await callback.message.edit_text(await texts.menu_text(locale), reply_markup=await kbs.menu_inline_kb(lang))


@dp.callback_query_handler(lambda call: call.data.endswith('lang'), state="*")
async def language_set(callback: types.CallbackQuery, locale):
    # await callback.message.delete()
    await callback.message.edit_text(await texts.start_text(locale), reply_markup=await kbs.start_inline_kb(locale))
    # await callback.message.answer_photo(MEDIA['about'], reply_markup=await kbs.start_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("back"), state='*')
async def back_menu(callback: types.CallbackQuery, locale, state: FSMContext):
    print("HELLOOOOO")
    print("&&&&&&&&&&&&&", callback.data)
    async with state.proxy() as data:
        data.clear()
        await state.finish()
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(await texts.menu_text(locale), reply_markup=await kbs.menu_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("menu"), state='*')
async def main_menu(callback: types.CallbackQuery, locale):
    print("#$#$#$#$#$#$#$", callback.data)
    await callback.answer()
    # await callback.message.delete()
    await callback.message.edit_text(await texts.menu_text(locale), reply_markup=await kbs.menu_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("register"), state='*')
async def register_func(callback: types.CallbackQuery, locale):
    print("CCCCCCCCCCCCCCCCCCCCCCCC", callback.data)
    await SetRegister.center.set()
    await callback.answer("THIS")
    await callback.message.delete()
    await callback.message.answer_photo(
        MEDIA.get('centers'),
        reply_markup=await kbs.register_inline_kb(locale),
        caption=await texts.register_list_text(locale)
    )


@dp.callback_query_handler(lambda call: call.data.endswith("courses"), state='*')  # END WITH
async def register_func(callback: types.CallbackQuery, locale):
    print("@@@@@@@@@@@@@@@@@@@@@@@@", callback.data)
    await SetRegister.course.set()
    await callback.answer("THIS")
    await callback.message.delete()
    await callback.message.answer_photo(
        MEDIA.get('courses'),
        reply_markup=await kbs.courses_inline_kb(locale),
        caption=await texts.courses_text(locale)
    )
    await SetRegister.course.set()


@dp.callback_query_handler(lambda call: call.data.endswith("contacts"), state='*')
async def register_func(callback: types.CallbackQuery, locale):
    print("@#@#@#@#@#@#@#@#@#@#", callback.data)
    await callback.answer("THIS")
    await callback.message.edit_text(await texts.contact_text(locale), parse_mode="HTML",
                                     reply_markup=await kbs.contacts_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("about"), state='*')
async def menu_func(callback: types.CallbackQuery, locale):
    print("ASDSDSA", callback.data)
    # await callback.answer()
    await callback.message.delete()
    # await callback.message.edit_text(await texts.about_text), reply_markup=await kbs.about_inline_kb(locale=locale))
    await callback.message.answer_photo(MEDIA['about'], reply_markup=await kbs.about_inline_kb(locale),
                                        caption=await texts.about_text(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("reg"), state="*")
async def reg_couse_func(callback: types.CallbackQuery, locale):
    print("@@@##########@@@@@@@@")
    await callback.message.delete()
    await callback.message.answer(_("Iltimos, to'liq ismingizni kiriting", locale),
                                  reply_markup=await kbs.reply_back(locale))
    await SetRegister.fio.set()


@dp.edited_message_handler()
async def msg_handler(message: types.Message):
    print(message)


@dp.pre_checkout_query_handler()
async def pre():
    print("PRE")


@dp.my_chat_member_handler()
async def some_handler(my_chat_member: types.ChatMemberUpdated):
    print(my_chat_member)


@dp.chat_member_handler()
async def some_handler(chat_member: types.ChatMemberUpdated):
    print("BAOBAB", chat_member)


@dp.message_handler(content_types=configs.all_content_types)
async def some_text(message: types.Message):
    print("DADA", message)
    if message.photo:
        print(message.photo)
    print(configs.LANG_STORAGE)
    await handlers.some_text_handler(message, bot)


@dp.pre_checkout_query_handler(lambda shipping_query: True)
async def some_pre_checkout_query_handler(shipping_query: types.ShippingQuery):
    print("shipping", shipping_query)


@dp.shipping_query_handler(lambda shipping_query: True)
async def some_shipping_query_handler(shipping_query: types.ShippingQuery):
    print("EEE", shipping_query)


@dp.errors_handler()
async def some_error(baba, error):
    print("error", baba, error)


@dp.callback_query_handler(state="*")
async def some_callback(callback: types.CallbackQuery, state: FSMContext, locale):
    await callback.answer()
    photo_dict = {
        "frontend": (MEDIA.get('frontend'), await texts.web_text(locale)),
        "backend": (MEDIA.get('backend'), await texts.backend_text(locale)),
        "android": (MEDIA.get("android"), await texts.android_text(locale)),
        "robots": (MEDIA.get('robots'), await texts.robots_text(locale)),
        "graphics": (MEDIA.get('graphic'), await texts.graphics_text(locale)),
        "english": (MEDIA.get('english'), await texts.english_text(locale)),
        "smm": (MEDIA.get('smm'), await texts.smm_text(locale)),
        "scratch": (MEDIA.get('scratch'), await texts.scratch_text(locale)),

        "course": MEDIA.get('courses'),
        "yakkasaroy": (MEDIA.get('yakkasaroy'), await texts.filial_yakkasaroy(locale)),
        "tashkent": (MEDIA.get('tashkent'), await texts.filial_tashkent(locale)),
        "chilonzor": (MEDIA.get('chilonzor'), await texts.filial_chilonzor(locale)),
        "mirzo": (MEDIA.get('mirzo'), await texts.filial_mirzo(locale)),
        "sergeli": (MEDIA.get('sergeli'), await texts.filial_sergeli(locale)),
        "bektemir": (MEDIA.get('bektemir'), await texts.filial_bektemir(locale)),
    }

    level_data, target_data = callback.data.split(":")
    async with state.proxy() as data:
        data[level_data] = target_data
        print("GAAAAAAAAAAAAAAAAAA", data)
        if not data.get('courses'):
            await callback.message.delete()
            await callback.message.answer_photo(photo_dict[data.get('register')][0],
                                                reply_markup=await kbs.courses_inline_kb(locale),
                                                caption=photo_dict[data.get('register')][1])
        elif not data.get('register'):
            await callback.message.delete()
            await callback.message.answer_photo(photo_dict['course'], reply_markup=await kbs.register_inline_kb(locale),
                                                caption=await texts.register_list_text(locale))
        else:
            print("ASDSDS")
            await callback.message.delete()
            await callback.message.answer_photo(photo=photo_dict[data['courses']][0],
                                                caption=photo_dict[data['courses']][1],
                                                reply_markup=await kbs.reg_inline_kb(locale),
                                                )
    print("##################", callback)


if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=configs.on_startup,
                           on_shutdown=configs.on_shutdown, skip_updates=True)
