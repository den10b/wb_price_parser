from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from filters.user import IsNotRegistered
from keyboards.callback_factory import ActionCallbackFactory
from keyboards.inline import register, back_button
from utils.db import add_user_ya, add_user_wb
from utils.wb_api import wb_check_token
from utils.ya_api import checkToken as ya_check_token

guest_router = Router()
guest_router.message.filter(IsNotRegistered())
guest_router.callback_query.filter(IsNotRegistered())


class States(StatesGroup):
    input_wb_jwt = State()
    input_ya_id = State()
    input_ya_token = State()


@guest_router.message(Command("start"))
async def handler(message: Message, state: FSMContext):
    await message.answer(f"👋 Привет!\n"
                         f"Пора зарегистрироваться\n"
                         f"Где вы торгуете?", reply_markup=await register())
    await state.clear()


@guest_router.callback_query(ActionCallbackFactory.filter(F.action == "exit"))
async def handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await state.clear()
    except:
        pass
    try:
        await call.message.delete_reply_markup()
    except:
        pass


@guest_router.callback_query(ActionCallbackFactory.filter(F.action == "register_wb"))
async def handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete_reply_markup()
    except:
        pass
    await state.set_state(States.input_wb_jwt)
    await call.message.answer(f"👋 Брат!\n"
                              f"Введи свой jwt:", reply_markup=await back_button())


@guest_router.message(States.input_wb_jwt)
async def handler(message: Message, state: FSMContext):
    try:
        is_token_valid = await wb_check_token(message.text)
    except:
        is_token_valid = False

    if is_token_valid:
        await add_user_wb(message.from_user.id, message.text)
        await message.answer(f"👋 Cпасибо!\n"
                             f"Вы зарегистрированы теперь как продавец на WB")
        await message.answer(f"Напишите /start, чтобы скорректировать цену своего товара")
    else:
        await message.answer(f"К сожалению, ваш токен не подходит\n"
                             f"Попробуйте еще раз", reply_markup=await back_button())


@guest_router.callback_query(ActionCallbackFactory.filter(F.action == "register_ya"))
async def handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete_reply_markup()
    except:
        pass
    await state.set_state(States.input_ya_id)
    await call.message.answer(f"👋 Хауди Хо!\n"
                              f"Введи свой id:", reply_markup=await back_button())


@guest_router.message(States.input_ya_id)
async def handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(f"Неверный формат!\n"
                             f"Попробуйте еще разок:", reply_markup=await back_button())
        return
    await state.update_data({"ya_id": message.text})
    await state.set_state(States.input_ya_token)
    await message.answer(f"👋 Спасибо!\n"
                         f"Теперь введите свой token:", reply_markup=await back_button())


@guest_router.message(States.input_ya_token)
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()
    ya_id = data.get("ya_id")
    try:
        is_token_valid = await ya_check_token(business_id=ya_id, oauth_token=message.text)
    except:
        is_token_valid = False
    if is_token_valid:
        await add_user_ya(message.from_user.id, message.text, ya_id)
        await message.answer(f"👋 Cпасибо!\n"
                             f"Вы зарегистрированы теперь как продавец на Яндекс Маркет")
        await message.answer(f"Напишите /start, чтобы скорректировать цену своего товара")
    else:
        await message.answer(f"К сожалению, ваш токен не подходит\n"
                             f"Попробуйте еще раз", reply_markup=await back_button())
