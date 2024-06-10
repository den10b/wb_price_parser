from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

import bot
from utils.wb_parser import parse

cmd_router = Router()


class States(StatesGroup):
    input_file = State()


@cmd_router.message(Command("sstart"))
async def handler(message: Message, state: FSMContext):
    res = await parse(["https://www.wildberries.ru/catalog/195932394/detail.aspx",
                       'https://www.wildberries.ru/catalog/165446363/detail.aspx',
                       'https://www.wildberries.ru/catalog/197029144/detail.aspx'])
    for tup in res:
        await message.answer(f"Артикул: {tup[0]}\n"
                             f"Цена: {tup[1]}₽")
    await state.clear()


@cmd_router.message(Command("start"))
async def handler(message: Message, state: FSMContext):
    await message.answer(f"👋 Добрый день!\n"
                         f"Жду ссылки на товары через запятую:")
    await state.clear()
    await state.set_state(States.input_file)


@cmd_router.message(States.input_file)
async def handler(message: Message, state: FSMContext):
    all_links = message.text.split(',')
    wb_links = []
    ya_links = []
    mega_links = []
    for link in all_links:
        if "www.wildberries.ru" in link:
            wb_links.append(link)
        if "megamarket.ru" in link:
            mega_links.append(link)
        if "market.yandex.ru" in link:
            ya_links.append(link)
    wb_parsed = await parse(wb_links)
    for tup in wb_parsed:
        await message.answer(f"Артикул: {tup[0]}\n"
                             f"Цена: {tup[1]}₽")
    await state.clear()
