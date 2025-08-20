#!/usr/bin/env python3
"""
Скрипт запуска для PythonAnywhere
Обрабатывает переменные окружения и запускает бота
"""

import os
import sys
from pathlib import Path

# Добавляем текущую директорию в путь
sys.path.insert(0, str(Path(__file__).parent))

# Проверяем обязательные переменные окружения
required_vars = ['BOT_TOKEN', 'ADMIN_ID']
missing_vars = []

for var in required_vars:
    if not os.getenv(var):
        missing_vars.append(var)

if missing_vars:
    print(f"❌ Ошибка: Отсутствуют обязательные переменные окружения: {', '.join(missing_vars)}")
    print("Настройте их в PythonAnywhere → Files → .env")
    sys.exit(1)

print("✅ Все переменные окружения настроены")
print("🚀 Запуск Telegram бота...")

# Импортируем и запускаем бота
try:
    from bot import TelegramBot
    bot = TelegramBot()
    print("🤖 Бот успешно запущен!")
    print("📱 Отправьте /start в Telegram")
    bot.run()
except Exception as e:
    print(f"❌ Ошибка запуска бота: {e}")
    sys.exit(1) 