from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from database import get_top_users

ranking_router = Router()


@ranking_router.message(Command("ranking"))
async def ranking_handler(message: Message):
    users = get_top_users(10)
    
    if not users:
        await message.answer("❌ Foydalanuvchilar topilmadi.")
        return
    
    text = "<b>🏆 TOP 10 REYTING</b>\n\n"
    
    for idx, user in enumerate(users, 1):
        user_id, username, balance, level = user
        medal = "🥇" if idx == 1 else "🥈" if idx == 2 else "🥉" if idx == 3 else f"{idx}️⃣"
        text += f"{medal} <b>{username}</b>\n   💰 {balance} coin | 📊 Level {level}\n\n"
    
    await message.answer(text)
