FROM python:3.11-slim

WORKDIR /app

# System kutubxonalarni o'rnatish (Pillow uchun)
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

# Python kutubxonalarni o'rnatish
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodlarni o'rnatish
COPY . .

# Botni ishga tushirish
CMD ["python", "main.py"]
