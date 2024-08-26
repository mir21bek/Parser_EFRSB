import sys
print(sys.path)
import contextlib
import asyncio
import re

from aiogram.client.bot import DefaultBotProperties
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
import logging

from handlers import admins
from filters.adminfilter import IsAdminFilter, IsUserFilter
from cfg.database import Database


db = Database("bot/cfg/database.db")



async def start():
    logging.basicConfig(level=logging.DEBUG, format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s')
    bot: Bot = Bot(token=db.get_all_config()[1], default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    # СОБЫТИЯ ДЛЯ АДМИНА
    dp.message.register(admins.list_users_task, F.text == "Список пользователей", IsAdminFilter())

    dp.message.register(admins.add_user_task, F.text == 'Добавить пользователя', IsAdminFilter())
    dp.message.register(admins.add_user_2_task, F.text.regexp(re.compile(r'Добавить (\d+)')), IsAdminFilter())

    dp.message.register(admins.del_user_task, F.text == 'Удалить пользователя', IsAdminFilter())
    dp.message.register(admins.del_user_2_task, F.text.regexp(re.compile(r'Удалить (\d+)')), IsAdminFilter())

    dp.message.register(admins.start_admin_task, Command(commands=["start"]), IsAdminFilter())

    dp.message.register(admins.parser_1_task, F.text == "Спарсить", IsUserFilter())
    dp.message.register(admins.parser_a_1_task, F.text == "Спарсить", IsAdminFilter())

    dp.message.register(admins.parser_2_task, F.document, IsUserFilter())
    dp.message.register(admins.parser_a_2_task, F.document, IsAdminFilter())

    dp.message.register(admins.start_users_task, Command(commands=["start"]), IsUserFilter())

    dp.message.register(admins.not_command_a_task, F.text, IsAdminFilter())
    dp.message.register(admins.not_command_task, F.text, IsUserFilter())

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as ex:
        logging.error(f'[Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    with contextlib.suppress(KeyboardInterrupt, SystemExit):
        asyncio.run(start())
