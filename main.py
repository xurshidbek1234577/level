import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from config import BOT_TOKEN

# HANDLERS import
from app.handlers import (
    start_router,
    profile_router,
    missions_router,
    ranking_router,
    shop_router,
    settings_router,
    admin_router,
)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Bot
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher
dp = Dispatcher()


async def main():
    logging.info("🚀 UPGRADE ishga tushdi...")

    # Routers ulash
    dp.include_router(start_router)
    dp.include_router(profile_router)
    dp.include_router(missions_router)
    dp.include_router(ranking_router)
    dp.include_router(shop_router)
    dp.include_router(settings_router)
    dp.include_router(admin_router)

    # eski update'larni tozalash
    await bot.delete_webhook(drop_pending_updates=True)

    # botni ishga tushirish
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi.")
