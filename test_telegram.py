#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестовый скрипт для проверки отправки сообщений в Telegram
"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    print("❌ Ошибка: TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не установлены в .env")
    exit(1)

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

# Тестовое сообщение
message = """🔔 <b>Тестовое сообщение</b>

Это тестовая заявка для проверки работы бота.

👤 <b>Имя:</b> Тестовый пользователь
📞 <b>Телефон:</b> +7 (999) 123-45-67
🕐 <b>Время:</b> Тест"""

print(f"📤 Отправка тестового сообщения...")
print(f"   Бот: {TELEGRAM_BOT_TOKEN[:20]}...")
print(f"   Chat ID: {TELEGRAM_CHAT_ID}")

try:
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    
    response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
    result = response.json()
    
    if result.get('ok'):
        print("✅ Сообщение успешно отправлено в Telegram!")
        print(f"   Message ID: {result.get('result', {}).get('message_id')}")
    else:
        print("❌ Ошибка отправки сообщения:")
        print(f"   {result}")
        if result.get('error_code') == 400:
            print("\n💡 Возможные причины:")
            print("   - Chat ID неправильный")
            print("   - Бот не запущен (напишите боту /start)")
        elif result.get('error_code') == 401:
            print("\n💡 Возможные причины:")
            print("   - Токен бота неправильный")
            
except Exception as e:
    print(f"❌ Ошибка: {e}")

