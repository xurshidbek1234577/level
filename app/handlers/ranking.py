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

    for idx, user in enumerate(users, start=1):
        user_id, username, balance, level, xp = user

        if idx == 1:
            medal = "🥇"
        elif idx == 2:
            medal = "🥈"
        elif idx == 3:
            medal = "🥉"
        else:
            medal = f"{idx}."

        if not username:
            username = f"ID:{user_id}"

        text += (
            f"{medal} <b>{username}</b>\n"
            f"💰 Coin: {balance}\n"
            f"📊 Level: {level}\n"
            f"⭐ XP: {xp}\n\n"
        )

    await message.answer(text, parse_mode="HTML")
