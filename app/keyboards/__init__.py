from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

# Main Menu
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="👤 Profil", callback_data="profile")],
        [InlineKeyboardButton(text="🎯 Missiyalar", callback_data="missions")],
        [InlineKeyboardButton(text="🏆 Reyting", callback_data="ranking")],
        [InlineKeyboardButton(text="🏅 Yutuqlar", callback_data="achievements")],
        [InlineKeyboardButton(text="⚙️ Sozlamalar", callback_data="settings")],
    ])
    return kb

# Profile Menu
def profile_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎴 Profil Kartasi", callback_data="profile_card")],
        [InlineKeyboardButton(text="📊 Statistika", callback_data="profile_stats")],
        [InlineKeyboardButton(text="⭐ Stat Ajratish", callback_data="allocate_stats")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")],
    ])
    return kb

# Missions Menu
def missions_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🟢 Oson", callback_data="missions_easy")],
        [InlineKeyboardButton(text="🟡 O'rta", callback_data="missions_normal")],
        [InlineKeyboardButton(text="🔴 Qiyin", callback_data="missions_hard")],
        [InlineKeyboardButton(text="📋 Faol Missiyalar", callback_data="active_missions")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")],
    ])
    return kb

# Accept Mission
def accept_mission(mission_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Qabul Qilish", callback_data=f"accept_mission_{mission_id}")],
        [InlineKeyboardButton(text="❌ Bekor Qilish", callback_data="missions")],
    ])
    return kb

# Complete Mission
def complete_mission(mission_id):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Tugallash", callback_data=f"complete_mission_{mission_id}")],
        [InlineKeyboardButton(text="❌ Bekor Qilish", callback_data="active_missions")],
    ])
    return kb

# Ranking Menu
def ranking_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏆 Top 10 Level", callback_data="ranking_level")],
        [InlineKeyboardButton(text="💰 Top 10 Coin", callback_data="ranking_coin")],
        [InlineKeyboardButton(text="⚡ Top 10 XP", callback_data="ranking_xp")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")],
    ])
    return kb

# Achievements Menu
def achievements_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🏅 Mening Yutuqlarim", callback_data="my_achievements")],
        [InlineKeyboardButton(text="📚 Barcha Yutuqlar", callback_data="all_achievements")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")],
    ])
    return kb

# Settings Menu
def settings_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔔 Bildirishnomalar", callback_data="settings_notifications")],
        [InlineKeyboardButton(text="🌙 Qoraqaranliq", callback_data="settings_dark_mode")],
        [InlineKeyboardButton(text="📝 Profil O'zgartirish", callback_data="settings_profile")],
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data="main_menu")],
    ])
    return kb

# Back Button
def back_button(callback_data):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Orqaga", callback_data=callback_data)],
    ])
    return kb
