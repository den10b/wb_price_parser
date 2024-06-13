import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.memory import MemoryStorage
from beanie import init_beanie
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient

import config
import handlers
from models import User
from pyvirtualdisplay import Display

storage = MemoryStorage()
main_bot = Bot(token=config.MAIN_BOT_TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
main_dp = Dispatcher(storage=storage)
display = Display(visible=0, size=(1920, 1080))
display.start()

async def init_db() -> None:
    docker_url = f"mongodb://{config.DB_USER}:{config.DB_PASS}@db:27017/{config.DB_NAME}?authSource=admin"
    local_url = f"mongodb://{config.DB_USER}:{config.DB_PASS}@localhost:27777/{config.DB_NAME}?authSource=admin"
    try:
        client = AsyncIOMotorClient(local_url)
        await init_beanie(database=client.get_database(), document_models=[User])
    except:
        pass
    try:
        client = AsyncIOMotorClient(docker_url)
        await init_beanie(database=client.get_database(), document_models=[User])
    except:
        pass


async def on_startup():
    await init_db()
    await asyncio.sleep(1)


async def main():
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
        display.stop()
        logger.error("Bot stopped!")
