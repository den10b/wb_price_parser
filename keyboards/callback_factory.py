from aiogram.filters.callback_data import CallbackData


class ActionCallbackFactory(CallbackData, prefix='action'):
    action: str