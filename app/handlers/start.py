from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

try:
    from database import add_user
except ImportError as e:
    print(f"❌ Database import xatosi: {e}")
    raise

start_router = Router()


@start_router.message(Command("start"))
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or f"User{user_id}"
    
    add_user(user_id, username)
    
    await message.answer(
        f"👋 Salom, <b>{username}</b>!\n\n"
        "🎮 Bu - <b>UPGRADE BOT</b>\n\n"
        "<b>📋 Mavjud komandalari:</b>\n"
        "/profile - Profilingizni ko'rish\n"
        "/card - Profil kartani rasm shaklida ko'rish\n"
        "/addxp [mikdor] - XP qo'shish\n"
        "/alloc [stat] [mikdor] - Statni ajratish\n"
        "/ranking - Top 10 reyting\n"
        "/help - Yordam\n\n"
        "🚀 Boshlash uchun /profile ni bosing!"
    )
