from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import bot

cmd_router = Router()


class States(StatesGroup):
    input_file = State()

@cmd_router.message(Command("start"))
async def handler(message: Message, state: FSMContext):
    await message.answer(f"👋 Добрый день! 👋\n"
                         f"Жду csv файл с ссылками на товары:")
    await state.clear()
    await state.set_state(States.input_file)


@cmd_router.message(States.input_file)
async def handler(message: Message, state: FSMContext):
    file_id = message.document.file_id
    res=await bot.main_bot.get_file(file_id)
    await message.answer(f"downloaded: {res.model_dump()}")

