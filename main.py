import asyncio
import logging

from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Message
from aiogram.filters import Command

from config import BOT_TOKEN
from database import init_db, add_user, get_user, update_balance, get_top_users

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


# /start komandasi
@dp.message(Command("start"))
async def start(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or "User"
    
    add_user(user_id, username)
    
    await message.answer(
        f"👋 Salom, <b>{username}</b>!\n\n"
        "Bu - Upgrade Bot 🚀\n\n"
        "<b>Mavjud komandalari:</b>\n"
        "/profile - Profilingizni ko'rish\n"
        "/balance - Balansni ko'rish\n"
        "/add - Balansga pul qo'shish\n"
        "/ranking - Top 10 reyting\n"
        "/help - Yordam"
    )


# /profile komandasi
@dp.message(Command("profile"))
async def profile(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi. /start ni bosing.")
        return
    
    user_id, username, balance, level, is_premium = user
    premium_text = "✨ Premium" if is_premium else "Oddiy"
    
    await message.answer(
        f"<b>👤 Profil</b>\n\n"
        f"👤 Ism: <b>{username}</b>\n"
        f"💰 Balans: <b>{balance}</b>\n"
        f"📊 Level: <b>{level}</b>\n"
        f"🎖️ Status: <b>{premium_text}</b>"
    )


# /balance komandasi
@dp.message(Command("balance"))
async def balance(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi. /start ni bosing.")
        return
    
    balance = user[2]
    await message.answer(f"💰 <b>Sizning balans:</b> {balance}")


# /add komandasi
@dp.message(Command("add"))
async def add(message: Message):
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer("❌ Foydalanish: /add <summa>\nMisol: /add 100")
        return
    
    try:
        amount = int(args[1])
        if amount <= 0:
            await message.answer("❌ Summa 0 dan katta bo'lishi kerak!")
            return
            
        user_id = message.from_user.id
        update_balance(user_id, amount)
        user = get_user(user_id)
        new_balance = user[2]
        
        await message.answer(
            f"✅ <b>Balans yangilandi!</b>\n"
            f"➕ Qo'shildi: <b>{amount}</b>\n"
            f"💰 Yangi balans: <b>{new_balance}</b>"
        )
    except ValueError:
        await message.answer("❌ Summa raqam bo'lishi kerak!")


# /ranking komandasi
@dp.message(Command("ranking"))
async def ranking(message: Message):
    users = get_top_users(10)
    
    if not users:
        await message.answer("❌ Foydalanuvchilar topilmadi.")
        return
    
    text = "<b>🏆 TOP 10 REYTING</b>\n\n"
    
    for idx, user in enumerate(users, 1):
        user_id, username, balance, level = user
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}."
        text += f"{medal} <b>{username}</b> - {balance} 💰\n"
    
    await message.answer(text)


# /help komandasi
@dp.message(Command("help"))
async def help_cmd(message: Message):
    await message.answer(
        "<b>❓ YORDAM</b>\n\n"
        "/start - Botni ishga tushirish\n"
        "/profile - Profilingizni ko'rish\n"
        "/balance - Balansni ko'rish\n"
        "/add <summa> - Balansga pul qo'shish\n"
        "/ranking - Top 10 ko'rsatish\n"
        "/help - Bu xabar"
    )


# Boshqa xabarlar
@dp.message()
async def echo(message: Message):
    await message.answer(
        "🤔 Noma'lum komanda.\n"
        "Mavjud komandalari ko'rish uchun /help ni bosing."
    )


async def main():
    # Database init
    init_db()
    logger.info("✅ Database initialized")
    
    logger.info("🚀 UPGRADE bot ishga tushdi...")
    
    # eski update'larni tozalash
    await bot.delete_webhook(drop_pending_updates=True)
    
    # botni ishga tushirish
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot to'xtatildi.")
