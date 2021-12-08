import asyncio
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
import logging

from tg_bot.config import load_config
from tg_bot.filters.admin import AdminFilter
from tg_bot.handlers.admin import register_admin
from tg_bot.handlers.start import register_commands

logger = logging.getLogger(__name__)


def register_all_middlewares(dp):
    dp.setup_middleware()  # Здесь подставлять названия мидвари и вызывать их через "()") )


def register_all_filters(dp):
    dp.filters_factory.bind(AdminFilter)  # Здесь подставлять названия через запятую фильтров)


def register_all_handlers(dp):
    register_admin(dp)
    register_commands(dp)
    # Здесь регистрировать хендлеры, а не в init как раньше
    # register_admin(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s'
    )
    logger.info("Starting bot")
    config = load_config(".env.dict")

    bot = Bot(token=config.tg_bot.token, parse_mode="HTML")
    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    dp = Dispatcher(bot, storage=storage)
    bot['config'] = config
    # В хендлере, если понадобиться объект из config, то можно будет
    # написать bot.get("config") и достануться все объекты конфига

    # register_all_middlewares(dp) Нужно будет раскадировать
    register_all_filters(dp)
    register_all_handlers(dp)

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
