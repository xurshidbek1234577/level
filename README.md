# Telegram Bot - UPGRADE 🎮

Upgrade Bot - bu Telegram uchun o'yin boti bo'lib, foydalanuvchilarga:
- 📊 Level tizimi
- ⚡ XP sistema
- 💪 Statistika (Strength, Agility, Intelligence)
- 💰 Balans va ko'p boshqa xususiyatlari mavjud.

## 🚀 Ishga tushirish

### 1. Talablarni o'rnatish

```bash
pip install -r requirements.txt
```

### 2. .env faylini sozlash

`.env` faylini oching va Telegram Bot tokeningizni qo'shing:

```dotenv
BOT_TOKEN=YOUR_BOT_TOKEN_HERE
```

Bot tokenini olish uchun [@BotFather](https://t.me/botfather) ga murojaat qiling.

### 3. Botni ishga tushirish

```bash
python main.py
```

## 📋 Komandalar

| Komanda | Tavsif |
|---------|--------|
| `/start` | Botni ishga tushirish va qisqacha yordam |
| `/profile` | Profilingizni text shaklida ko'rish |
| `/card` | Profil kartasini rasm shaklida ko'rish |
| `/addxp [mikdor]` | XP qo'shish (Misol: `/addxp 50`) |
| `/alloc [stat] [mikdor]` | Statni ajratish (Misol: `/alloc strength 5`) |
| `/ranking` | Top 10 eng yaxshi foydalanuvchilar |
| `/help` | Barcha komandalarni ko'rish |

## 📂 Loyiha Tuzilishi

```
level/
├── main.py                 # Asosiy skript
├── config.py              # Konfiguratsiya
├── database.py            # Ma'lumotlar bazasi logikasi
├── requirements.txt       # Kutubxonalar
├── .env                   # Maxfiy konfiguratsiya
├── .gitignore            # Git uchun e'lon qilinmaydigan fayllar
└── app/
    ├── __init__.py
    ├── handlers/
    │   ├── __init__.py
    │   ├── start.py       # /start handler
    │   ├── profile.py     # /profile, /card, /addxp, /alloc
    │   ├── missions.py    # /missions (future)
    │   ├── ranking.py     # /ranking
    │   ├── shop.py        # /shop (future)
    │   ├── settings.py    # /settings (future)
    │   └── admin.py       # /admin (future)
    └── utils/
        ├── __init__.py
        └── image.py       # Profil kartani generatsiya qilish
```

## 🛠️ Venv va Dependencies

### Linux/Mac

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 🐳 Docker bilan ishga tushirish

### Dockerfile yaratish

Dockerfile fayli allaqachon mavjud bo'lsa, quyidagini bajaring:

```bash
docker build -t upgrade-bot .
docker run -d --name upgrade-bot upgrade-bot
```

### Docker Compose bilan

```bash
docker-compose up -d
```

## 🔒 Xavfsizlik

- **`.env` faylini git'dan ko'rib chiqishdan saqlang** - `.gitignore` faylida `.env` allaqachon qo'shilgan
- **BOT_TOKEN ni hech kimga bermang** - bu sizning botingizning paroliyigina
- **Database fayllar (`*.db`) ga ehtiyot bilan munosabat qiling**

## 📊 Database

SQLite3 ma'lumotlar bazasi qo'llaniladi. Database avtomatik yaratiladi.

### Jadvallar

**users** - Foydalanuvchi ma'lumotlari:
- user_id (PRIMARY KEY)
- username
- balance
- level
- xp
- xp_needed
- hp, mp
- strength, agility, intelligence
- stat_points
- is_premium

**transactions** - Tranzaksiyalar tarixi

## 🔄 Kelajakda

- [ ] Missiyalar sistema
- [ ] Shop - predmetlarni sotib olish
- [ ] Admin panel
- [ ] Sozlamalar
- [ ] PvP sistema
- [ ] Guild sistema

## 📞 Aloqa

Savollaringiz bo'lsa, @xurshidbek1234577 ga murojaat qiling.

---

**Enjoy the game! 🎮**
