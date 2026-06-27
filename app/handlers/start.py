```python
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import CommandStart

from database import add_user

start_router = Router()

# Asosiy menyu
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👤 Profil"),
            KeyboardButton(text="🎯 Missiyalar"),
        ],
        [
            KeyboardButton(text="🏆 Reyting"),
            KeyboardButton(text="🛒 Do'kon"),
        ],
        [
            KeyboardButton(text="🎁 Daily Bonus"),
            KeyboardButton(text="⚙️ Sozlamalar"),
        ],
    ],
    resize_keyboard=True,
    one_time_keyboard=False,
    input_field_placeholder="Kerakli bo'limni tanlang..."
)


@start_router.message(CommandStart())
async def start_handler(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username or message.from_user.first_name

    add_user(user_id, username)

    await message.answer(
        f"👋 Xush kelibsiz, <b>{username}</b>!\n\n"
        "🚀 <b>UPGRADE BOT</b>\n\n"
        "O'zingizni rivojlantirishni hoziroq boshlang.\n"
        "👇 Quyidagi menyudan foydalaning.",
        reply_markup=main_keyboard
    )
```
