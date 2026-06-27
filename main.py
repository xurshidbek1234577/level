```python
import asyncio
import logging
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import BOT_TOKEN
from database import init_db

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from app.handlers import (
    start_router,
    profile_router,
    missions_router,
    ranking_router,
    shop_router,
    settings_router,
    admin_router,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp = Dispatcher()


async def main():
    init_db()
    logger.info("✅ Database initialized")

    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(missions_router)
    dp.include_router(ranking_router)
    dp.include_router(shop_router)
    dp.include_router(settings_router)
    dp.include_router(admin_router)

    await bot.delete_webhook(drop_pending_updates=True)

    logger.info("🚀 Bot ishga tushdi...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi.")
```
