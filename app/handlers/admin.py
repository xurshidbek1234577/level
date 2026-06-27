from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

admin_router = Router()


@admin_router.message(Command("admin"))
async def admin_handler(message: Message):
    await message.answer(
        "👨‍💼 <b>ADMIN PANEL</b>\n\n"
        "⏳ Bu funksiyalar keyingi versiyada qo'shiladi...\n\n"
        "👈 Bosh menyu: /start"
    )
