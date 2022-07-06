import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.exceptions import BotBlocked, BotKicked, UserDeactivated
from aiogram.utils.executor import start_webhook

import configs
import kbs
import texts
from configs import SetRegister

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

# webhook settings
WEBHOOK_HOST = configs.SITE_URL
WEBHOOK_PATH = '/webhook/'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = configs.WEBHOOK_PORT


class SetReport(StatesGroup):
    report = State()


class SetState(StatesGroup):
    lang = State()


@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, locale, state: FSMContext):
    arguments = message.get_args()
    if arguments == "":
        async with state.proxy() as data:
            data.clear()
        x = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
        await x.delete()
        if await configs.collusers.count_documents({"id": message.from_user.id}) < 1:
            await message.answer(texts.start_text,
                                 reply_markup=await kbs.start_inline_kb(locale),
                                 parse_mode="HTML")  # required use bot.send_message!
        else:
            await message.answer(texts.menu_text,
                                 reply_markup=await kbs.menu_inline_kb(locale))
    else:
        from uuid import UUID
        uuid_obj = UUID(arguments)
        link = await configs.collinks.find_one({"url": uuid_obj})
        async with state.proxy() as data:
            pipeline = [
                {
                    "$lookup": {
                        'from': 'courses_centers',
                        'localField': 'center_id',
                        'foreignField': 'id',
                        'as': 'center'
                    }
                },
                {"$unwind": "$center"},
                {
                    "$lookup":
                        {
                            'from': 'courses_courses',
                            'localField': 'course_id',
                            'foreignField': 'id',
                            'as': 'course'
                        }
                },
                {"$unwind": "$course"},
                {
                    '$match': {
                        'course.id': link['course_id'],
                        'center.id': link['center_id'],
                    }
                },
                {
                    '$project':
                        {
                            'course': 1,
                            'center': 1
                        }
                }
            ]

            async for doc in (configs.collinks.aggregate(pipeline)):
                data['external'] = doc
            await SetRegister.fio.set()
            about_course = await configs.collcourses.find_one({'slug': data['external'].get('course')['slug']})
            if about_course:
                description = about_course['description_uz'] if locale == "uz" else about_course['description_ru']

                await message.answer_photo(about_course['image'], caption=description)
                return await message.answer("Iltimos FIO yozing")
            else:
                return await message.answer(texts.empty_about_page)


@dp.message_handler(commands=["main"])
async def menu(message: types.Message, locale, state: FSMContext):
    await message.answer(texts.menu_text,
                         reply_markup=await kbs.menu_inline_kb(locale))


@dp.message_handler(commands="centers", state="*")
async def centers_menu(message: types.Message, locale, state: FSMContext):
    x = await message.answer(".", reply_markup=types.ReplyKeyboardRemove())
    await x.delete()
    await kbs.register_inline_kb(locale, message=message)


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
            external = data.get('external')
            if external:
                await message.answer(_("Sizning murojaatingiz qabul qilindi"))
                return await kbs.submit_message(bot, configs.GROUP_ID, locale, data, True)
            await kbs.submit_message(bot, message.from_user.id, locale, data)
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
            await kbs.submit_message(bot, configs.GROUP_ID, locale, data)
            await state.finish()
        else:
            await state.finish()
            await callback.message.answer(_("Ro'yxatdan o'tish bekor qilindi!"))
            return await menu(callback.message, locale, state)


@dp.callback_query_handler(lambda call: call.data.startswith('lang'), state="*")
async def language_set(callback: types.CallbackQuery, locale):
    await callback.answer()
    lang = callback.data.split(":")[1]
    if await configs.collusers.count_documents({"id": callback.from_user.id}) < 1:
        await configs.collusers.insert_one({"id": callback.from_user.id, "lang": lang})
    else:
        configs.collusers.update_one({"id": int(callback.from_user.id)}, {
            "$set": {"lang": lang}})
    configs.LANG_STORAGE[callback.from_user.id] = lang
    await callback.message.edit_text(texts.menu_text, reply_markup=await kbs.menu_inline_kb(lang))


@dp.callback_query_handler(lambda call: call.data.endswith('lang'), state="*")
async def language_set(callback: types.CallbackQuery, locale):
    await callback.answer()
    await callback.message.edit_text(texts.start_text, reply_markup=await kbs.start_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("back"), state='*')
async def back_menu(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    get_state = await state.get_state()
    await callback.message.delete()
    if get_state == "SetRegister:center":
        await callback.message.answer(texts.menu_text, reply_markup=await kbs.menu_inline_kb(locale))
    else:
        await callback.message.answer(texts.start_text, reply_markup=await kbs.start_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("menu"), state='*')
async def main_menu(callback: types.CallbackQuery, locale, state: FSMContext):
    print("14", await state.get_state())
    await callback.answer()
    # await callback.message.delete()
    await callback.message.edit_text(texts.menu_text, reply_markup=await kbs.menu_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("register"), state='*')
async def register_func(callback: types.CallbackQuery, locale, state: FSMContext):
    print("15", await state.get_state())
    await callback.answer()
    await SetRegister.center.set()
    await callback.message.delete()
    await kbs.register_inline_kb(locale, callback.message)


@dp.callback_query_handler(lambda call: call.data.endswith("courses"))  # END WITH
async def register_func(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    await kbs.courses_inline_kb(locale, callback.message)
    await SetRegister.confirm.set()


@dp.callback_query_handler(lambda call: call.data.endswith("contacts"), state='*')
async def register_func(callback: types.CallbackQuery, locale):
    await callback.answer()
    await kbs.contacts_inline_kb(locale, callback.message)


@dp.callback_query_handler(lambda call: call.data.endswith("about"), state='*')
async def menu_func(callback: types.CallbackQuery, locale):
    await callback.answer()
    await callback.message.delete()
    # await callback.message.edit_text(await texts.about_text), reply_markup=await kbs.about_inline_kb(locale=locale))
    await kbs.about_inline_kb(locale, callback.message)


@dp.callback_query_handler(state=SetRegister.confirm)
async def reg_course_func(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    async with state.proxy() as data:
        data['courses'] = callback.data.split(":")[1]

    if len(data) < 2:
        await kbs.reg_inline_kb(locale, callback.message, data)
        await SetRegister.center.set()
        print("@@@@@@@@2")
    else:
        await kbs.reg_inline_kb(locale, callback.message, data)
        await SetRegister.fio.set()
        print("@@@@@@@@1")


@dp.callback_query_handler(state=SetRegister.fio)
async def fio_set(callback: types.CallbackQuery, locale, state: FSMContext):
    await callback.answer()
    await callback.message.delete()
    async with state.proxy() as data:
        data['register'] = callback.data.split(":")[1]
    await callback.message.answer(texts.fio_answer_text, reply_markup=await kbs.reply_back(locale))


@dp.callback_query_handler(lambda call: call.data.startswith("answer"), state="*")
async def report_callback(callback: types.CallbackQuery, state: FSMContext, locale):
    await callback.answer()
    await callback.message.answer(_("Iltimos, o'z shikoyat/taklif'ingizni jo'nating", locale=locale),
                                  reply_markup=await kbs.reply_back(locale))
    async with state.proxy() as data:
        data['answer'] = callback.data.split(":")[1]
    await SetReport.report.set()


@dp.callback_query_handler(lambda call: call.data.endswith("report"), state="*")
async def report_callback(callback: types.CallbackQuery, locale):
    print("22")
    await callback.answer()
    # await callback.message.delete()
    await callback.message.answer(_("Iltimos, o'z shikoyat/taklif'ingizni jo'nating", locale=locale),
                                  reply_markup=await kbs.reply_back(locale))
    await SetReport.report.set()


@dp.message_handler(state=SetReport.report, content_types=['text'])
async def report_handler(message: types.Message, state: FSMContext, locale):
    async with state.proxy() as data:
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
    if message.photo:
        await message.answer(message.photo[-1].file_id)
    await message.answer(_("Botni qayta yoqish uchun /start ni bosing."))


#
# @dp.errors_handler()
# async def some_error(baba, error):
#     logging.error("error", baba, error)


@dp.callback_query_handler(state=SetRegister.course)
async def mninini(callback: types.CallbackQuery, locale, state: FSMContext):
    print("BAURJAN")
    await callback.answer()
    await callback.message.delete()
    await kbs.reg_inline_kb(locale, callback.message, await state.get_data())
    await SetRegister.fio.set()


@dp.callback_query_handler(state=SetRegister.center)
async def manamana(callback: types.CallbackQuery, locale, state: FSMContext):
    print("26", callback.data)
    await callback.answer()
    # await callback.message.delete()
    await callback.message.delete()
    async with state.proxy() as data:
        key, value = callback.data.split(":")
        data['register'] = value
        if not data.get('courses', None):
            print("27", "####")
            await kbs.courses_inline_kb(locale, callback.message)
            await SetRegister.confirm.set()
            print("@@@@@@@@2")
        else:
            await SetRegister.fio.set()
            print("ROOOOOOOOOOD")
            await kbs.register_inline_kb(locale, callback.message)


@dp.callback_query_handler(state="*")
async def some_callback(callback: types.CallbackQuery, state: FSMContext, locale):
    print("27", await state.get_state())
    print("POKA TUT")
    await callback.answer()


if __name__ == '__main__':
    # if not configs.DEBUG:
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=configs.on_startup,
        on_shutdown=configs.on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
    # else:
    #     executor.start_polling(dp,
    #                            on_startup=configs.on_startup,
    #                            on_shutdown=configs.on_shutdown, skip_updates=True)
