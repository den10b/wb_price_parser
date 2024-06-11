import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from loguru import logger

import config
import handlers

from models import User
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

storage = MemoryStorage()
main_bot = Bot(token=config.MAIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
dp = Dispatcher(storage=storage)


async def init_db() -> None:
    mongo = AsyncIOMotorClient("mongodb://db:27017/")
    await init_beanie(database=mongo.your_db_name, document_models=[User])


async def on_startup():
    await init_db()
    await asyncio.sleep(1)


async def main():
    main_dp = Dispatcher(storage=storage)

    logger.info('Регистрирую Middlewares.')
    logger.info('Регистрирую Handlers.')
    handlers.setup(main_dp)
    logger.info('Запускаю бота.')

    await on_startup()
    try:
        await main_bot.delete_webhook(drop_pending_updates=True)
        await main_dp.start_polling(main_bot)
    finally:
        await main_bot.session.close()

    await main_bot.delete_webhook(drop_pending_updates=True)
    await main_dp.start_polling(main_bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
