from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

shop_router = Router()


@shop_router.message(Command("shop"))
async def shop_handler(message: Message):
    await message.answer(
        "🛍️ <b>SHOP</b>\n\n"
        "⏳ Bu funksiyalar keyingi versiyada qo'shiladi...\n\n"
        "👈 Bosh menyu: /start"
    )
