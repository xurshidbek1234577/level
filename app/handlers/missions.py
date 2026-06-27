from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

missions_router = Router()


@missions_router.message(Command("missions"))
async def missions_handler(message: Message):
    await message.answer(
        "🎯 <b>MISSIYALAR</b>\n\n"
        "⏳ Bu funksiyalar keyingi versiyada qo'shiladi...\n\n"
        "👈 Bosh menyu: /start"
    )
