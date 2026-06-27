from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

settings_router = Router()


@settings_router.message(Command("settings"))
async def settings_handler(message: Message):
    await message.answer(
        "⚙️ <b>SOZLAMALAR</b>\n\n"
        "⏳ Bu funksiyalar keyingi versiyada qo'shiladi...\n\n"
        "👈 Bosh menyu: /start"
    )
