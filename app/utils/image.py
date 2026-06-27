from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os


def generate_profile_card(user):
    """
    Profil kartasini generatsiya qiladi
    user: (user_id, username, balance, level, xp, xp_needed, hp, mp, strength, agility, intelligence, stat_points, is_premium, created_at)
    """
    user_id, username, balance, level, xp, xp_needed, hp, mp, strength, agility, intelligence, stat_points, is_premium, created_at = user
    
    # Rasm o'lchamlari
    width, height = 600, 800
    background_color = (20, 20, 40)  # Qora siniy fon
    
    # Rasm yaratish
    img = Image.new('RGB', (width, height), background_color)
    draw = ImageDraw.Draw(img)
    
    # Ranglar
    primary_color = (100, 200, 255)
    accent_color = (255, 200, 100)
    text_color = (255, 255, 255)
    premium_color = (255, 215, 0)
    
    # XP bar o'lchamlari
    bar_width = 500
    bar_height = 30
    bar_x = 50
    
    # Title
    draw.text((width // 2 - 80, 30), "⚔️ PROFIL KARTASI ⚔️", fill=accent_color)
    
    # Username va Premium badge
    premium_text = " ✨ PREMIUM" if is_premium else ""
    draw.text((50, 80), f"👤 {username}{premium_text}", fill=text_color)
    
    # Level va Balance
    y_offset = 130
    draw.text((50, y_offset), f"📊 Level: {level}", fill=primary_color)
    draw.text((300, y_offset), f"💰 Balance: {balance}", fill=accent_color)
    
    # XP Bar
    y_offset += 50
    draw.rectangle([bar_x, y_offset, bar_x + bar_width, y_offset + bar_height], 
                   outline=primary_color, width=2)
    
    xp_percentage = (xp / xp_needed) * bar_width
    draw.rectangle([bar_x, y_offset, bar_x + xp_percentage, y_offset + bar_height], 
                   fill=primary_color)
    
    draw.text((bar_x + 10, y_offset + 5), f"XP: {xp}/{xp_needed}", fill=text_color)
    
    # Stats
    y_offset += 80
    draw.text((50, y_offset), "⚡ STATISTIKA", fill=accent_color)
    
    y_offset += 50
    draw.text((50, y_offset), f"❤️  HP: {hp}", fill=(255, 100, 100))
    y_offset += 40
    draw.text((50, y_offset), f"🔵 MP: {mp}", fill=(100, 150, 255))
    y_offset += 40
    draw.text((50, y_offset), f"💪 Strength: {strength}", fill=(255, 165, 0))
    y_offset += 40
    draw.text((50, y_offset), f"🎯 Agility: {agility}", fill=(100, 255, 100))
    y_offset += 40
    draw.text((50, y_offset), f"🧠 Intelligence: {intelligence}", fill=(200, 100, 255))
    y_offset += 40
    draw.text((50, y_offset), f"⭐ Stat Points: {stat_points}", fill=accent_color)
    
    # Footer
    draw.text((50, height - 50), f"ID: {user_id}", fill=(150, 150, 150))
    
    # Rasm BytesIO ga o'zlash
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    
    return img_byte_arr
