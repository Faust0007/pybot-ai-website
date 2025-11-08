#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Локальный веб-сервер для PyBot AI
Запускает простой HTTP сервер для просмотра сайта
"""

import http.server
import socketserver
import sys
import webbrowser
from pathlib import Path

# Порт по умолчанию
DEFAULT_PORT = 8000

def start_server(port=DEFAULT_PORT):
    """Запускает локальный веб-сервер"""
    
    # Проверяем наличие index.html
    if not Path('index.html').exists():
        print("❌ Ошибка: файл index.html не найден!")
        print("Убедитесь, что вы запускаете скрипт из директории с файлами сайта.")
        sys.exit(1)
    
    # Создаем обработчик запросов
    handler = http.server.SimpleHTTPRequestHandler
    
    # Настраиваем обработчик для правильной работы с CSS и JS
    class CustomHandler(handler):
        def end_headers(self):
            # Добавляем заголовки для правильной работы с современными браузерами
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
            super().end_headers()
    
    try:
        # Создаем сервер
        with socketserver.TCPServer(("", port), CustomHandler) as httpd:
            server_url = f"http://localhost:{port}"
            
            print("=" * 60)
            print("🚀 PyBot AI - Локальный веб-сервер запущен!")
            print("=" * 60)
            print(f"📍 Адрес: {server_url}")
            print(f"📁 Директория: {Path.cwd()}")
            print("=" * 60)
            print("\n💡 Сайт доступен по адресу:")
            print(f"   → {server_url}")
            print("\n💡 Для доступа с других устройств в вашей сети:")
            print(f"   → http://<ваш-ip-адрес>:{port}")
            print("\n⚠️  Для остановки сервера нажмите Ctrl+C")
            print("=" * 60)
            print()
            
            # Автоматически открываем браузер
            try:
                webbrowser.open(server_url)
                print("🌐 Браузер открыт автоматически...\n")
            except Exception as e:
                print(f"⚠️  Не удалось открыть браузер автоматически: {e}\n")
                print(f"   Откройте вручную: {server_url}\n")
            
            # Запускаем сервер
            httpd.serve_forever()
            
    except OSError as e:
        if "Address already in use" in str(e) or e.errno == 98:
            print(f"❌ Ошибка: Порт {port} уже занят!")
            print(f"💡 Попробуйте использовать другой порт:")
            print(f"   python server.py {port + 1}")
            sys.exit(1)
        else:
            print(f"❌ Ошибка при запуске сервера: {e}")
            sys.exit(1)
    except KeyboardInterrupt:
        print("\n\n" + "=" * 60)
        print("🛑 Сервер остановлен")
        print("=" * 60)
        sys.exit(0)

def main():
    """Главная функция"""
    # Проверяем аргументы командной строки для порта
    port = DEFAULT_PORT
    
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if port < 1 or port > 65535:
                raise ValueError("Порт должен быть в диапазоне 1-65535")
        except ValueError as e:
            print(f"❌ Ошибка: Неверный номер порта - {e}")
            print(f"💡 Использование: python server.py [порт]")
            print(f"   Пример: python server.py 8080")
            sys.exit(1)
    
    start_server(port)

if __name__ == "__main__":
    main()

