from aiogram.filters import BaseFilter
from aiogram.types import Message
from cfg.database import Database


db = Database("bot/cfg/database.db")


class IsAdminFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        admins = db.get_all_config()[2].split(",")
        return f"{message.from_user.id}" in admins


class IsUserFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        users = db.get_all_config()[3].split(",")
        return f"{message.from_user.id}" in users
