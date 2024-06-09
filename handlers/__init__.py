from aiogram import Dispatcher

from .user import cmd_router


def setup(main_dp: Dispatcher):
    main_dp.include_router(cmd_router)

