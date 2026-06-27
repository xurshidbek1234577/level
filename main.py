import asyncio
import logging
import sys
import os

# Python path'ni sozlash
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import BOT_TOKEN
from database import init_db

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# HANDLERS import
try:
    from app.handlers import (
        start_router,
        profile_router,
        missions_router,
        ranking_router,
        shop_router,
        settings_router,
        admin_router,
    )
except ImportError as e:
    print(f"❌ Handler import xatosi: {e}")
    sys.exit(1)

# Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Bot
bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

# Dispatcher
dp = Dispatcher()


async def main():
    try:
        # Database init
        init_db()
        logger.info("✅ Database initialized")
        
        logger.info("🚀 UPGRADE ishga tushdi...")

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
        logger.info("📡 Polling boshlanmoqda...")
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    except Exception as e:
        logger.error(f"❌ Xatolik: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⏹️ Bot to'xtatildi.")
    except Exception as e:
        logger.error(f"❌ Ishlamay qoldi: {e}", exc_info=True)
        sys.exit(1)
