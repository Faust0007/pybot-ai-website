#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Сервер для обработки заявок с сайта и отправки уведомлений в Telegram
Можно задеплоить на Render, Railway, Heroku или любой другой хостинг
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os
from datetime import datetime
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

app = Flask(__name__)

# Настройка CORS для вашего сайта
ALLOWED_ORIGINS = [
    'https://faust0007.github.io',
    'http://localhost:8000',  # Для локального тестирования
    'http://127.0.0.1:8000'   # Для локального тестирования
]

CORS(app, origins=ALLOWED_ORIGINS, supports_credentials=True)

# Конфигурация Telegram бота из .env файла
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Проверка наличия обязательных переменных
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN не установлен! Проверьте .env файл")
if not TELEGRAM_CHAT_ID:
    raise ValueError("TELEGRAM_CHAT_ID не установлен! Проверьте .env файл")

TELEGRAM_API_URL = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'

@app.route('/api/submit', methods=['POST'])
def submit_form():
    """Обработка заявки с сайта"""
    try:
        data = request.get_json()
        name = data.get('name', '').strip()
        phone = data.get('phone', '').strip()
        
        # Валидация
        if not name or not phone:
            return jsonify({
                'success': False,
                'error': 'Имя и телефон обязательны для заполнения'
            }), 400
        
        # Формируем сообщение для Telegram
        message = f"""🔔 <b>Новая заявка с сайта PyBot AI</b>

👤 <b>Имя:</b> {name}
📞 <b>Телефон:</b> {phone}
🕐 <b>Время:</b> {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

---
Сайт: PyBot AI"""

        # Отправляем в Telegram
        telegram_response = send_to_telegram(message)
        
        if telegram_response.get('ok'):
            return jsonify({
                'success': True,
                'message': 'Заявка успешно отправлена!'
            }), 200
        else:
            # Логируем ошибку, но все равно возвращаем успех пользователю
            print(f"Ошибка отправки в Telegram: {telegram_response}")
            return jsonify({
                'success': True,
                'message': 'Заявка получена!'
            }), 200
            
    except Exception as e:
        print(f"Ошибка обработки заявки: {e}")
        return jsonify({
            'success': False,
            'error': 'Произошла ошибка при обработке заявки'
        }), 500

def send_to_telegram(message):
    """Отправка сообщения в Telegram"""
    try:
        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }
        
        response = requests.post(TELEGRAM_API_URL, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return {'ok': False, 'error': str(e)}

@app.route('/health', methods=['GET'])
def health_check():
    """Проверка работоспособности сервера"""
    return jsonify({
        'status': 'ok',
        'bot_configured': bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID),
        'site_url': 'https://faust0007.github.io/pybot-ai-website/'
    }), 200

@app.route('/', methods=['GET'])
def index():
    """Главная страница API"""
    return jsonify({
        'service': 'PyBot AI Telegram Notification Server',
        'status': 'running',
        'endpoints': {
            '/api/submit': 'POST - Отправка заявки с сайта',
            '/health': 'GET - Проверка работоспособности'
        }
    }), 200

if __name__ == '__main__':
    # Для локального тестирования
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

