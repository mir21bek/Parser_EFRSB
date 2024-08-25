from aiogram import Bot
from aiogram.types import Message, FSInputFile

from cfg.database import Database
from keyboards import admin_kb


db = Database("bot/cfg/database.db")


async def start_admin_task(message: Message):
    await message.answer("Пивет админ!", reply_markup=admin_kb.start_a_reply())


async def start_users_task(message: Message):
    await message.answer(f"Пивет @{message.from_user.username}!", reply_markup=admin_kb.start_reply())


async def list_users_task(message: Message):
    all_info = list(filter(None, db.get_all_config()[3].split(",")))
    text = "Список всех пользователей:\n\n"
    for idx, info in enumerate(all_info):
        text += f"{idx+1}. <code>{info}</code>\n"

    await message.answer(text, reply_markup=admin_kb.start_a_reply())


async def add_user_task(message: Message):
    await message.answer("Введите:\n <code>Добавить</code> 1234567 (id пользователя)", reply_markup=admin_kb.start_a_reply())


async def add_user_2_task(message: Message):
    db.add_user(message.text.split(" ")[1])
    await message.answer("Пользователь добавлен!", reply_markup=admin_kb.start_a_reply())


async def del_user_task(message: Message):
    await message.answer("Введите:\n <code>Удалить</code> 1234567 (id пользователя)", reply_markup=admin_kb.start_a_reply())


async def del_user_2_task(message: Message):
    db.del_user(message.text.split(" ")[1])
    await message.answer("Пользователь удалён", reply_markup=admin_kb.start_a_reply())


async def not_command_a_task(message: Message):
    await message.answer("Такой команды нет(", reply_markup=admin_kb.start_a_reply())


async def not_command_task(message: Message):
    await message.answer("Такой команды нет(", reply_markup=admin_kb.start_reply())


async def parser_1_task(message: Message):
    doc_file = FSInputFile(path=f'../parserfile/excel/example.xlsx')
    await message.answer_document(document=doc_file, caption="Отправь Excel файл как в примере 👆", reply_markup=admin_kb.start_reply())


async def parser_a_1_task(message: Message):
    doc_file = FSInputFile(path=f'../parserfile/excel/example.xlsx')
    await message.answer_document(document=doc_file, caption="Отправь Excel файл как в примере 👆", reply_markup=admin_kb.start_a_reply())


async def parser_2_task(message: Message, bot: Bot):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"../parserfile/excel/{message.from_user.id}.xlsx")

    await message.answer(text="Начинается обработка и парсинг 🔄\nПарсинг одного пользователя ≈ 1мин\n\n<b>Не начинайте новый парсинг пока не завершиться этот!</b>", reply_markup=admin_kb.start_reply())
    db.add_file(message.from_user.id)


async def parser_a_2_task(message: Message, bot: Bot):
    file_id = message.document.file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, f"../parserfile/excel/{message.from_user.id}.xlsx")

    await message.answer(text="Начинается обработка и парсинг 🔄\nПарсинг одного пользователя ≈ 1мин\n\n<b>Не начинайте новый парсинг пока не завершиться этот!</b>", reply_markup=admin_kb.start_a_reply())
    db.add_file(message.from_user.id)
