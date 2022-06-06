import asyncio # noqa
import datetime
import glob  # noqa
import logging
import os

import motor.motor_tornado

from pathlib import Path
from typing import Tuple, Any

from aiogram import types
from aiogram.utils.exceptions import BotBlocked, BotKicked, UserDeactivated
from aiogram.contrib.middlewares.i18n import I18nMiddleware
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

# Main telegram bot configs
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Telegram chats
ADMIN_IDS = tuple(os.getenv("ADMIN_IDS").split(","))
GROUP_ID = int(os.getenv("GROUP_ID"))

# Language
LANG_STORAGE = {}
LANGS = ["ru", "uz"]
I18N_DOMAIN = "mybot"
BASE_DIR = Path(__file__).parent
LOCALES_DIR = BASE_DIR / "locales"

# Database
MONGO_URL = os.getenv("MONGO_URL", default="mongodb://localhost:27017/myapp")
cluster = motor.motor_tornado.MotorClient(MONGO_URL)
collusers = cluster.itpark.users
collreports = cluster.itpark.reports
collmedia = cluster.itpark.media
collbuttons = cluster.itpark.buttons

# Telegam supported types
all_content_types = ["text", "sticker", "photo",
                     "voice", "document", "video", "video_note"]

# MEDIA
MEDIA = {}

# Logging
if not os.getenv("DEBUG", default=False):
    formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
    logging.basicConfig(
        filename=f'logs/bot-from-{datetime.datetime.now().date()}.log',
        filemode='w',
        format=formatter,
        datefmt='%Y-%m-%d %H:%M:%S',
        level=logging.WARNING
    )


class Localization(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
        """
        User locale getter
        You can override the method if you want to use different way of getting user language.
        :param action: event name
        :param args: event arguments
        :return: locale name
        """
        user: types.User = types.User.get_current()

        if LANG_STORAGE.get(user.id) is None:
            LANG_STORAGE[user.id] = "en"
        *_, data = args
        language = data['locale'] = LANG_STORAGE[user.id]
        return language


# On start polling telegram this function running
async def on_startup(dp):
    users_lang = collusers.find({}, {"_id": 1, "lang": 1})
    print(await dp.bot.get_me())
    logging.warning("BOT STARTED")
    async for i in users_lang:
        LANG_STORAGE[i.get("_id")] = i.get("lang", "ru")

    media = collmedia.find({})
    async for i in media:
        MEDIA[i.get("_id")] = i.get('file_id')
    for i in ADMIN_IDS:
        try:
            # for filename in glob.glob('media/*.jpg'):
            #     with open(os.path.join(os.getcwd(), filename), 'rb') as f:  # open in readonly mode
            #         print(filename)
            #         x = await dp.bot.send_photo(5252535217, types.InputFile(filename))
            #         await collmedia.update_one({"_id": filename.split("/")[1].replace(".jpg", "")},
            #                                    {"$set": {"file_id": x.photo[-1].file_id}})
            #         try:
            #             await collmedia.insert_one({"_id": filename.split("/")[1].replace(".jpg", ""),
            #                                         "file_id": x.photo[-1].file_id})
            #         except:
            #             print("PASS")
            await dp.bot.send_message(i, "Bot are start!")
        except (BotKicked, BotBlocked, UserDeactivated):
            pass


# On stop polling Telegram, this function running and stopping polling's
async def on_shutdown(dp):
    logging.warning("Shutting down..")
    for i in ADMIN_IDS:
        try:
            await dp.bot.send_message(i, "Bot are shutting down!")
        except (BotKicked, BotBlocked, UserDeactivated):
            pass
    await dp.storage.close()
    await dp.storage.wait_closed()
    logging.warning("Bye!")

