from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.mongo import MongoStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils.callback_data import CallbackData

import admin_commands
import configs
import handlers
import kbs
import texts

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


@dp.message_handler(commands="start", state="*")
async def cmd_start(message: types.Message, locale):
    print("ASDASDAS")
    # print(await configs.collusers.count_documents({"_id": message.from_user.id}))
    # print(await configs.collusers.find_one({}))
    if await configs.collusers.count_documents({"_id": message.from_user.id}) < 1:
        await SetState.lang.set()
        await message.answer(_(texts.start_text, locale=locale),
                             reply_markup=await kbs.start_inline_kb(locale),
                             parse_mode="HTML")  # required use bot.send_message!
    else:
        await message.answer(_(texts.menu_text, locale=locale),
                             reply_markup=await kbs.menu_inline_kb(locale))


@dp.message_handler(commands="lang")
async def cmd_lang(message: types.Message, locale):
    await message.answer(
        _("Your current language: <i>{language}</i>").format(language=locale)
    )


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


@dp.message_handler(text=_("One"))
async def text_one(message: types.Message):
    await message.answer(_("Really one"))


@dp.message_handler(text=_("Two"))
async def text_two(message: types.Message):
    await message.answer(_("Really two"))


@dp.message_handler(text=_("Three"))
async def text_three(message: types.Message):
    await message.answer(_("Really three"))


@dp.message_handler(commands='lang')
async def cmd_lang(message: types.Message, locale):
    # print(locale)
    # For setting custom lang you have to modify i18n middleware
    await message.reply(_('Your current language: <i>{language}</i>').format(language=locale))


@dp.message_handler(commands=["main"])
async def menu(message: types.Message):
    print("LOW", message)
    await handlers.menu_handler(message)


@dp.message_handler(commands=['post'])
async def post(message: types.Message):
    data = {'type': 'text', 'text': 'text', 'entities': None}
    users = 390736292,
    await admin_commands.send_post_all_users(data, users, bot)


@dp.message_handler(commands=["report"])
async def report(message: types.Message):
    await SetReport.report.set()
    await message.answer("Bizga o'z takliflaringizni yuboring!")


@dp.message_handler(state=SetReport.report,
                    content_types=configs.all_content_types)
async def report_process(message: types.Message, state: FSMContext):
    await handlers.report_process_handler(message, state, bot)


@dp.callback_query_handler(lambda call: call.data.startswith('lang'), state=SetState.lang)
async def language_set(callback: types.CallbackQuery, state: FSMContext):
    lang = callback.data.split(":")[1]

    configs.LANG_STORAGE[callback.from_user.id] = lang
    configs.collusers.update_one({"_id": int(callback.from_user.id)}, {
        "$set": {"lang": lang}})
    await callback.answer(_("Selected", locale=lang))
    # await callback.message.delete()
    await callback.message.edit_text(texts.menu_text)
    await callback.message.edit_reply_markup(await kbs.menu_inline_kb(lang))

    await state.finish()

    # await callback.message.answer(texts.menu_text, reply_markup=await kbs.menu_inline_kb(lang))

    # await state.finish()
    # await cmd_start(message=callback, locale=lang)


@dp.callback_query_handler(lambda call: call.data.endswith("back"), state='*')
async def main_menu(callback: types.CallbackQuery, locale):
    print("HELLOOOOO")
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer(_(texts.menu_text), reply_markup=await kbs.menu_inline_kb(locale))


@dp.callback_query_handler(lambda call: call.data.endswith("register"), state='*')
async def register_func(callback: types.CallbackQuery, locale):
    await callback.answer("THIS")
    await callback.message.delete()
    await callback.message.answer_photo(
        "AgACAgIAAxkBAAICEmKNPlr4Z4n3XFFoy9TUFa09iSufAALcujEbvlBpSC8VhjNUbvryAQADAgADeQADJAQ",
        reply_markup=await kbs.register_inline_kb(locale),
        caption=_(texts.register_list_text)
    )


@dp.callback_query_handler(lambda call: call.data.endswith("about"), state='*')
async def menu_func(callback: types.CallbackQuery, locale):
    print("ASDSDSA", callback)
    await callback.answer()
    await callback.message.edit_text(_(texts.about_text))
    await callback.message.edit_reply_markup(await kbs.about_inline_kb(locale=locale))


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


@dp.callback_query_handler(lambda callback_query: True)
async def some_callback(callback: types.CallbackQuery):
    print(callback)


if __name__ == '__main__':
    executor.start_polling(dp,
                           on_startup=configs.on_startup,
                           on_shutdown=configs.on_shutdown, skip_updates=True)
