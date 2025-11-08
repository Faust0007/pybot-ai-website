#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для быстрого деплоя на Netlify через CLI
Требует установки Netlify CLI: npm install -g netlify-cli
"""

import subprocess
import sys
import os
from pathlib import Path

def check_netlify_cli():
    """Проверяет, установлен ли Netlify CLI"""
    try:
        result = subprocess.run(['netlify', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print(f"✅ Netlify CLI установлен: {result.stdout.strip()}")
            return True
    except FileNotFoundError:
        return False
    return False

def install_netlify_cli():
    """Предлагает установить Netlify CLI"""
    print("❌ Netlify CLI не установлен")
    print("\n📦 Для установки выполните одну из команд:")
    print("   npm install -g netlify-cli")
    print("   или")
    print("   yarn global add netlify-cli")
    print("\n💡 Если у вас нет Node.js, установите его с https://nodejs.org")
    return False

def deploy_to_netlify():
    """Деплоит сайт на Netlify"""
    
    # Проверяем наличие файлов
    required_files = ['index.html', 'styles.css', 'script.js']
    missing_files = [f for f in required_files if not Path(f).exists()]
    
    if missing_files:
        print(f"❌ Отсутствуют файлы: {', '.join(missing_files)}")
        return False
    
    print("=" * 60)
    print("🚀 Деплой на Netlify")
    print("=" * 60)
    print()
    
    # Проверяем, авторизован ли пользователь
    try:
        result = subprocess.run(['netlify', 'status'], 
                              capture_output=True, 
                              text=True)
        if 'Logged in' not in result.stdout:
            print("🔐 Требуется авторизация в Netlify")
            print("Выполняется: netlify login")
            subprocess.run(['netlify', 'login'])
    except Exception as e:
        print(f"⚠️  Ошибка проверки авторизации: {e}")
    
    # Деплой
    print("\n📤 Начинаем деплой...")
    print("💡 При первом запуске вам нужно будет:")
    print("   1. Выбрать 'Create & configure a new site'")
    print("   2. Выбрать команду сборки (оставьте пустым для статического сайта)")
    print("   3. Указать директорию публикации: . (точка)")
    print()
    
    try:
        subprocess.run(['netlify', 'deploy', '--prod'], check=True)
        print("\n✅ Деплой завершен успешно!")
        print("🌐 Ваш сайт доступен в интернете!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Ошибка при деплое: {e}")
        return False
    except KeyboardInterrupt:
        print("\n\n🛑 Деплой отменен пользователем")
        return False

def main():
    """Главная функция"""
    print("=" * 60)
    print("🌐 Netlify Deploy Helper")
    print("=" * 60)
    print()
    
    if not check_netlify_cli():
        if not install_netlify_cli():
            sys.exit(1)
        return
    
    print()
    response = input("Продолжить деплой? (y/n): ").strip().lower()
    if response != 'y':
        print("Деплой отменен")
        sys.exit(0)
    
    deploy_to_netlify()

if __name__ == "__main__":
    main()

