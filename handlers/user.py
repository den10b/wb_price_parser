from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import asyncio

from filters.user import IsRegistered
from keyboards.callback_factory import ActionCallbackFactory
from keyboards.inline import ok_button
from utils.wb_parser import parse as wb_parse
from utils.megamarket_parser import parse as mega_parse
from utils.yandex_parser import yandex_parser as ya_parse
from utils.wb_api import wb_check_current_price, wb_change_price
from utils.db import get_user

import re

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


'''@user_router.message(Command("sstart"))
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
'''


@user_router.message(Command("start"))
async def handler(message: Message, state: FSMContext):
    await message.answer(f"👋 Добрый день!\n"
                         f"Жду артикул вашего товара:")
    await state.clear()
    await state.set_state(States.input_my_id)


@user_router.message(States.input_my_id)
async def handler(message: Message, state: FSMContext):
    try:
        nm_price = await wb_check_current_price((await get_user(message.from_user.id)).wb_jwt, message.text)
    except:
        nm_price = 0

    if nm_price:
        await state.set_data({"nm_id": message.text})

        await message.answer(f"Супер!\n"
                             f"Текущая цена вашего товара: {nm_price}")
        await message.answer(f"Теперь отправьте ссылки на товары ваших конкурентов через пробел или запятую\n"
                             f"Сейчас мы поддерживаем только WB. Я.Маркет, Мегамаркет")
        await state.set_state(States.input_links)
    else:
        await message.answer(f"Что-то пошло не так :(\n"
                             f"Попробуйте снова ввести ваш артикул")


@user_router.message(States.input_links)
async def handler(message: Message, state: FSMContext):
    async def parse_func_call(market_name: str, links_list, parse_func):
        if not links_list:
            return
        parsed_list = await parse_func(links_list)
        if not parsed_list:
            return
        sum_price = 0

        await message.answer(f'Товары с {market_name}')
        for tup in parsed_list:
            sum_price += tup[0]
            await message.answer(f"Артикул: {tup[1]}\n"
                                 f"Цена: {tup[0]}₽")
        return sum_price, len(parsed_list)

    pattern = r"""(?:https?:\/\/|ftps?:\/\/|www\.)(?:(?![.,?!;:()]*(?:\s|$|"))[^\s"]){2,}"""
    # Разбиваем сообщение юзера на список ссылок
    all_links = re.findall(pattern, message.text.strip())
    wb_links, ya_links, mega_links = [], [], []
    for link in all_links:
        if "www.wildberries.ru" in link:
            wb_links.append(link)
        if "megamarket.ru" in link:
            mega_links.append(link)
        if "market.yandex.ru" in link:
            ya_links.append(link)

    all_markets_list = [await parse_func_call('Wildberries', wb_links, wb_parse),
                        await parse_func_call('Яндекс Маркет', ya_links, ya_parse),
                        await parse_func_call('Мегамаркет', mega_links, mega_parse)]

    all_market_price_sum = sum([i[0] if not i is None else 0 for i in all_markets_list])
    all_markets_nm_count = sum([i[1] if not i is None else 0 for i in all_markets_list])

    if all_market_price_sum and all_markets_nm_count:
        rounded_mean_price = round(all_market_price_sum / all_markets_nm_count)
        await message.answer(f"Средняя цена проанализированных товаров: {rounded_mean_price:.2f}\n"
                             f"Рекомендуемая цена: {rounded_mean_price * 0.9:.2f}₽", reply_markup=await ok_button())
        await state.set_data({"target_price": rounded_mean_price})

    else:
        await message.answer(f"Товары не удалось проанализироввать :(\n"
                             f"Попробуйте снова, отправьте /start")
    await state.clear()


@user_router.callback_query(ActionCallbackFactory.filter(F.action == "confirm"))
async def handler(call: types.CallbackQuery, state: FSMContext):
    market = (await get_user(call.message.chat.id)).market
    if market == 'wb':
        wb_token = (await get_user(call.message.chat.id)).wb_jwt
        nm_id = (await state.get_data())["nm_id"]
        target_price = (await state.get_data())['target_price']
        try:
            is_accepted = await wb_change_price(wb_token, nm_id, target_price)
        except:
            is_accepted = False

        if is_accepted:
            await call.message.answer(f"Цена успешно изменена!")
        else:
            await call.message.answer(f"К сожалению, не получилось изменить цену товара :(\n"
                                      f"Попробуйте снова, отправьте /start")
    await state.clear()

