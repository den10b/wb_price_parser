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
from utils.yandex_parser import yandex_parser as ya_parse

user_router = Router()
user_router.message.filter(IsRegistered())
user_router.callback_query.filter(IsRegistered())


class States(StatesGroup):
    input_my_id = State()
    input_links = State()


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
    await message.answer(f"Средняя цена: {summa / count:.2f}\n"
                         f"Цена: {(summa / count) * 0.9:.2f}₽")
    await state.clear()


@user_router.message(Command("start"))
async def handler(message: Message, state: FSMContext):
    await message.answer(f"👋 Добрый день!\n"
                         f"Жду артикул вашего товара:")
    await state.clear()
    await state.set_state(States.input_my_id)


@user_router.message(States.input_my_id)
async def handler(message: Message, state: FSMContext):
    await state.set_data({"nm_id": message.text})

    await message.answer(f"Супер!\n"
                         f"Теперь жду ссылки на товары через запятую:")
    await state.set_state(States.input_links)


@user_router.message(States.input_links)
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
        if wb_parsed:
            await message.answer(f"Товары с wildberries:")
            for tup in wb_parsed:
                summa += tup[1]
                count += 1
                await message.answer(f"Артикул: {tup[0]}\n"
                                     f"Цена: {tup[1]}₽")
    if ya_links:
        ya_parsed = await ya_parse(ya_links)
        if ya_parsed:
            await message.answer(f"Товары с Яндекс маркет:")
            for tup in ya_parsed:
                summa += tup[0]
                count += 1
                await message.answer(f"Артикул: {tup[1]}\n"
                                     f"Цена: {tup[0]}₽")
    if mega_links:
        mega_parsed = mega_parse(mega_links)
        if mega_parsed:
            await message.answer(f"Товары с megamarket:")
            for tup in mega_parsed:
                summa += tup[0]
                count += 1
                await message.answer(f"Артикул: {tup[1]}\n"
                                     f"Цена: {tup[0]}₽")
    if count == 0:
        count += 1
    if count and summa:
        rounded_mean = round(summa / count)
        await message.answer(f"Средняя цена: {rounded_mean:.2f}\n"
                             f"Рекомендуемая цена: {(rounded_mean) * 0.9:.2f}₽", reply_markup=await ok_button())

    else:
        await message.answer(f"Товары не удалось проанализироввать")
    await state.clear()


@user_router.callback_query(ActionCallbackFactory.filter(F.action == "confirm"))
async def handler(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer(f"Теперь надо бы цену товара обновить...")
