from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from io import BytesIO

from database import get_user, add_xp, allocate_stat
from app.utils.image import generate_profile_card

profile_router = Router()


@profile_router.message(Command("profile"))
async def profile_handler(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi. /start ni bosing.")
        return
    
    user_id, username, balance, level, xp, xp_needed, hp, mp, strength, agility, intelligence, stat_points, is_premium, created_at = user
    premium_text = "✨ PREMIUM" if is_premium else "📍 ODDIY"
    
    await message.answer(
        f"<b>👤 PROFIL</b>\n\n"
        f"👤 <b>Ism:</b> {username}\n"
        f"💰 <b>Balans:</b> {balance} coin\n"
        f"📊 <b>Level:</b> {level}\n"
        f"⚡ <b>XP:</b> {xp}/{xp_needed}\n"
        f"❤️ <b>HP:</b> {hp}\n"
        f"🔵 <b>MP:</b> {mp}\n"
        f"💪 <b>Strength:</b> {strength}\n"
        f"🎯 <b>Agility:</b> {agility}\n"
        f"🧠 <b>Intelligence:</b> {intelligence}\n"
        f"⭐ <b>Stat Points:</b> {stat_points}\n"
        f"🎖️ <b>Status:</b> {premium_text}"
    )


@profile_router.message(Command("card"))
async def card_handler(message: Message):
    user_id = message.from_user.id
    user = get_user(user_id)
    
    if not user:
        await message.answer("❌ Foydalanuvchi topilmadi. /start ni bosing.")
        return
    
    # Rasmni generatsiya qilish
    image_bytes = generate_profile_card(user)
    
    await message.answer_photo(
        photo=image_bytes,
        caption=f"🎴 {user[1]} ning profil kartasi"
    )


@profile_router.message(Command("addxp"))
async def addxp_handler(message: Message):
    args = message.text.split()
    
    if len(args) < 2:
        await message.answer("❌ Foydalanish: /addxp <mikdor>\nMisol: /addxp 50")
        return
    
    try:
        xp_amount = int(args[1])
        if xp_amount <= 0:
            await message.answer("❌ XP 0 dan katta bo'lishi kerak!")
            return
        
        user_id = message.from_user.id
        add_xp(user_id, xp_amount)
        user = get_user(user_id)
        
        await message.answer(
            f"✅ <b>XP qo'shildi!</b>\n"
            f"➕ {xp_amount} XP\n"
            f"📊 Level: {user[3]}\n"
            f"⚡ XP: {user[4]}/{user[5]}"
        )
    except ValueError:
        await message.answer("❌ XP raqam bo'lishi kerak!")


@profile_router.message(Command("alloc"))
async def alloc_handler(message: Message):
    args = message.text.split()
    
    if len(args) < 3:
        await message.answer(
            "❌ Foydalanish: /alloc <stat> <mikdor>\n"
            "Statlar: strength, agility, intelligence\n"
            "Misol: /alloc strength 5"
        )
        return
    
    try:
        stat_type = args[1].lower()
        amount = int(args[2])
        
        if stat_type not in ['strength', 'agility', 'intelligence']:
            await message.answer("❌ Stat turini to'g'ri kiriting: strength, agility, intelligence")
            return
        
        if amount <= 0:
            await message.answer("❌ Mikdor 0 dan katta bo'lishi kerak!")
            return
        
        user_id = message.from_user.id
        success = allocate_stat(user_id, stat_type, amount)
        
        if success:
            user = get_user(user_id)
            await message.answer(
                f"✅ <b>Stat ajratildi!</b>\n"
                f"📍 {stat_type.upper()}: +{amount}\n"
                f"⭐ Qolgan points: {user[11]}"
            )
        else:
            user = get_user(user_id)
            await message.answer(f"❌ Yetarli stat point'lar yo'q! (Mavjud: {user[11]})")
    except ValueError:
        await message.answer("❌ Mikdor raqam bo'lishi kerak!")
