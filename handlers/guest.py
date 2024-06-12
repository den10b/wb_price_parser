from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from filters.user import IsNotRegistered
from keyboards.callback_factory import ActionCallbackFactory
from keyboards.inline import register, back_button
from utils.db import add_user_ya, add_user_wb

guest_router = Router()
guest_router.message.filter(IsNotRegistered())
guest_router.callback_query.filter(IsNotRegistered())


class States(StatesGroup):
    input_wb_jwt = State()
    input_ya_id = State()
    input_ya_token = State()


@guest_router.message(Command("start"))
async def handler(message: Message, state: FSMContext):
    await message.answer(f"👋 Брат!\n"
                         f"Зарегайся пж\n"
                         f"Где ты продаешь?", reply_markup=await register())
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
    await add_user_wb(message.from_user.id, message.text)
    await message.answer(f"👋 спасибо Брат!\n"
                         f"Ты зареган теперь как продавец на вб")


@guest_router.callback_query(ActionCallbackFactory.filter(F.action == "register_ya"))
async def handler(call: types.CallbackQuery, state: FSMContext):
    try:
        await call.message.delete_reply_markup()
    except:
        pass
    await state.set_state(States.input_ya_id)
    await call.message.answer(f"👋 Брат!\n"
                              f"Введи свой id:", reply_markup=await back_button())


@guest_router.message(States.input_ya_id)
async def handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer(f"Не, Брат!\n"
                             f"попробуй еще разок:", reply_markup=await back_button())
        return
    await state.update_data({"ya_id": message.text})
    await state.set_state(States.input_ya_token)
    await message.answer(f"👋 спасибо Брат!\n"
                         f"Теперь введи свой token:", reply_markup=await back_button())


@guest_router.message(States.input_ya_token)
async def handler(message: Message, state: FSMContext):
    data = await state.get_data()
    ya_id = data.get("ya_id")
    await add_user_ya(message.from_user.id, message.text, ya_id)
    await message.answer(f"👋 спасибо Брат!\n"
                         f"Ты зареган теперь как продавец на маркете")
