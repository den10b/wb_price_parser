from aiogram.utils.keyboard import InlineKeyboardBuilder

from keyboards.callback_factory import ActionCallbackFactory


async def register():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text="WB", callback_data=ActionCallbackFactory(action="register_wb"))
    inline_keyboard.button(text="Yandex Market", callback_data=ActionCallbackFactory(action="register_ya"))
    inline_keyboard.adjust(1)
    return inline_keyboard.as_markup()


async def back_button():
    inline_keyboard = InlineKeyboardBuilder()
    inline_keyboard.button(text="❌ Отмена", callback_data=ActionCallbackFactory(action="exit"))
    return inline_keyboard.as_markup()
