from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from filters.user import IsRegistered
from keyboards.callback_factory import ActionCallbackFactory
from keyboards.inline import ok_button
from utils.wb_parser import parse as wb_parse
from utils.megamarket_parser import parse as mega_parse

user_router = Router()
user_router.message.filter(IsRegistered())
user_router.callback_query.filter(IsRegistered())


class States(StatesGroup):
    input_file = State()

@user_router.callback_query(ActionCallbackFactory.filter(F.action == "exit"))
async def handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.clear()
    except:
        pass
    try:
        await call.message.delete_reply_markup()
    except:
        pass

@user_router.message(Command("sstart"))
async def handler(message: Message, state: FSMContext):
    res = await wb_parse(["https://www.wildberries.ru/catalog/195932394/detail.aspx",
                       'https://www.wildberries.ru/catalog/165446363/detail.aspx',
                       'https://www.wildberries.ru/catalog/197029144/detail.aspx'])
    summa = 0
    count = 0
    for tup in res:
        summa += tup[1]
        count += 1
        await message.answer(f"Артикул: {tup[0]}\n"
                             f"Цена: {tup[1]}₽")
    await message.answer(f"Средняя цена: {summa / count}\n"
                         f"Цена: {(summa / count) * 0.9}₽")
    await state.clear()


@user_router.message(Command("start"))
async def handler(message: Message, state: FSMContext):
    await message.answer(f"👋 Добрый день!\n"
                         f"Жду ссылки на товары через запятую:")
    await state.clear()
    await state.set_state(States.input_file)


@user_router.message(States.input_file)
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

    summa = 0
    count = 0
    if wb_links:
        wb_parsed = await wb_parse(wb_links)
        await message.answer(f"Товары с wildberries:")
        for tup in wb_parsed:
            summa += tup[1]
            count += 1
            await message.answer(f"Артикул: {tup[0]}\n"
                                 f"Цена: {tup[1]}₽")
    if mega_links:
        mega_parsed = mega_parse(mega_links)
        await message.answer(f"Товары с megamarket:")
        for tup in mega_parsed:
            summa += tup[1]
            count += 1
            await message.answer(f"Артикул: {tup[0]}\n"
                                 f"Цена: {tup[1]}₽")

    await message.answer(f"Средняя цена: {summa / count}\n"
                         f"Рекомендуемая цена: {(summa / count) * 0.9}₽", reply_markup=await ok_button())
    await state.clear()
