from aiogram import Dispatcher

from .guest import guest_router
from .user import user_router


def setup(main_dp: Dispatcher):
    main_dp.include_router(user_router)
    main_dp.include_router(guest_router)
