import os
from dotenv import load_dotenv
import logging

# Загружаем переменные окружения из .env файла
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, os.getenv('LOG_LEVEL', 'INFO')),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# TELEGRAM BOT
# ============================================
BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', 0))

# Валидация обязательных параметров
if not BOT_TOKEN:
    raise ValueError("❌ BOT_TOKEN не установлен в .env файле!")
if not ADMIN_ID:
    raise ValueError("❌ ADMIN_ID не установлен в .env файле!")

logger.info("✅ Telegram конфигурация загружена")

# ============================================
# ПЛАТЕЖИ - ЮMONEY (YOOKASSA)
# ============================================
PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN', '')
YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID', '')
YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY', '')
CURRENCY = os.getenv('CURRENCY', 'RUB')
MIN_PAYMENT_AMOUNT = int(os.getenv('MIN_PAYMENT_AMOUNT', 100))
MAX_PAYMENT_AMOUNT = int(os.getenv('MAX_PAYMENT_AMOUNT', 999999))

# Проверка настроек платежей
if PAYMENT_PROVIDER_TOKEN:
    logger.info("✅ Payment provider token настроен")
else:
    logger.warning("⚠️ PAYMENT_PROVIDER_TOKEN не установлен. Платежи будут недоступны.")

if YOOKASSA_SHOP_ID and YOOKASSA_SECRET_KEY:
    logger.info("✅ YooKassa API ключи настроены")
else:
    logger.warning("⚠️ YooKassa ключи не настроены. API платежи будут недоступны.")

# ============================================
# БЕЗОПАСНОСТЬ
# ============================================
API_SECRET_KEY = os.getenv('API_SECRET_KEY', '')
API_URL = os.getenv('API_URL', 'http://localhost:8000')
MAX_REQUESTS_PER_MINUTE = int(os.getenv('MAX_REQUESTS_PER_MINUTE', 60))
REQUEST_TIMEOUT = int(os.getenv('REQUEST_TIMEOUT', 30))

if not API_SECRET_KEY:
    logger.warning("⚠️ API_SECRET_KEY не установлен. Используйте только для разработки!")
elif len(API_SECRET_KEY) < 32:
    logger.warning("⚠️ API_SECRET_KEY слишком короткий. Используйте минимум 32 символа!")

# ============================================
# БАЗА ДАННЫХ
# ============================================
DATABASE_PATH = os.getenv('DATABASE_PATH', 'bot_database.db')
AUTO_BACKUP = os.getenv('AUTO_BACKUP', 'True').lower() == 'true'
BACKUP_INTERVAL_HOURS = int(os.getenv('BACKUP_INTERVAL_HOURS', 24))

# ============================================
# БЕСПЛАТНЫЕ МАТЕРИАЛЫ
# ============================================
# Настройки для бесплатных материалов
FREE_MATERIALS = {
    'welcome_message': 'Добро пожаловать! Вот ваши бесплатные материалы:',
    'materials': [
        {
            'title': '📚 Основы метода работы',
            'url': os.getenv('MATERIAL_1_URL', 'https://teletype.in/@your_username/osnovy')
        },
        {
            'title': '🎯 Как и почему это работает',
            'url': os.getenv('MATERIAL_2_URL', 'https://teletype.in/@your_username/kak-rabotaet')
        },
        {
            'title': '💡 Практические советы',
            'url': os.getenv('MATERIAL_3_URL', 'https://teletype.in/@your_username/sovety')
        }
    ]
}

# Настройки для платных продуктов
PAID_PRODUCTS = {
    'basic_course': {
        'name': 'Базовый курс',
        'price': 5000,
        'description': 'Полный курс по основам метода'
    },
    'advanced_course': {
        'name': 'Продвинутый курс',
        'price': 10000,
        'description': 'Углубленное изучение продвинутых техник'
    }
}

# Настройки для анонимных вопросов
ANONYMOUS_QUESTION_LINK = os.getenv('ANONYMOUS_QUESTION_LINK', 'https://forms.google.com/your-form')

# Настройки для диагностических созвонов
DIAGNOSTIC_CALL_INFO = {
    'duration': '30 минут',
    'description': 'Бесплатный диагностический созвон для определения ваших потребностей'
} 