from aiogram import types
from aiogram.filters import BaseFilter

from utils.db import get_user


class IsRegistered(BaseFilter):
    """
    Зарегистрирован ли пользователь в боте.
    """
    is_registered: bool = True

    async def __call__(self, update: types.Message | types.CallbackQuery) -> bool:
        user = await get_user(update.from_user.id)
        if user:
            return True is self.is_registered
        return False is self.is_registered


class IsNotRegistered(BaseFilter):
    """
    Зарегистрирован ли пользователь в боте.
    """
    is_registered: bool = False

    async def __call__(self, update: types.Message | types.CallbackQuery) -> bool:
        user = await get_user(update.from_user.id)
        if user:
            return True is self.is_registered
        return False is self.is_registered
