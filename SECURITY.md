# 🔐 Руководство по безопасности

## 📋 Чеклист безопасности

### ✅ Обязательные меры

- [ ] Все секретные ключи в `.env` файле
- [ ] `.env` добавлен в `.gitignore`
- [ ] Уникальный `API_SECRET_KEY` сгенерирован
- [ ] HTTPS включен на всех доменах
- [ ] Валидация всех пользовательских данных
- [ ] Rate limiting на API эндпоинтах
- [ ] Регулярное резервное копирование БД

### 🔒 Рекомендуемые меры

- [ ] Двухфакторная аутентификация для админов
- [ ] Мониторинг подозрительной активности
- [ ] Логирование всех важных операций
- [ ] Ротация ключей каждые 90 дней
- [ ] Обновление зависимостей

## 🔑 Управление секретами

### Генерация безопасных ключей

```bash
# Секретный ключ для API (32 байта)
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Секретный ключ для API (64 байта - более надежный)
python -c "import secrets; print(secrets.token_urlsafe(64))"

# UUID для уникальных идентификаторов
python -c "import uuid; print(uuid.uuid4())"
```

### Структура .env файла

```env
# ============================================
# TELEGRAM BOT
# ============================================
BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
ADMIN_ID=123456789

# ============================================
# БЕЗОПАСНОСТЬ API
# ============================================
API_SECRET_KEY=ваш_супер_секретный_ключ_32_символа_минимум
API_URL=https://your-api.render.com

# ============================================
# ЮMONEY (YOOKASSA)
# ============================================
YOOKASSA_SHOP_ID=123456
YOOKASSA_SECRET_KEY=live_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
PAYMENT_PROVIDER_TOKEN=381764678:LIVE:xxxxxxxxxxxxx

# ============================================
# БАЗА ДАННЫХ
# ============================================
DATABASE_PATH=bot_database.db

# ============================================
# ОПЦИОНАЛЬНО
# ============================================
LOG_LEVEL=INFO
MAX_REQUESTS_PER_MINUTE=60
```

### ⚠️ Что НИКОГДА не добавлять в Git

```
.env
.env.local
.env.production
*.db
*.sqlite
private_keys/
secrets/
credentials.json
```

## 🛡️ Защита данных пользователей

### 1. Хранение персональных данных

```python
# database.py
import hashlib

def hash_phone_number(phone: str) -> str:
    """Хешируем номер телефона для безопасного хранения"""
    return hashlib.sha256(phone.encode()).hexdigest()

def store_user(user_id, phone, name):
    # Храним хеш вместо реального номера для индексации
    phone_hash = hash_phone_number(phone)
    # Реальный номер шифруем (опционально)
    # encrypted_phone = encrypt(phone, SECRET_KEY)
    ...
```

### 2. Валидация входных данных

```python
# handlers.py
import re

def validate_phone_number(phone: str) -> bool:
    """Проверка формата номера телефона"""
    pattern = r'^\+?[1-9]\d{10,14}$'
    return bool(re.match(pattern, phone))

def sanitize_input(text: str) -> str:
    """Очистка пользовательского ввода"""
    # Удаляем потенциально опасные символы
    return re.sub(r'[<>\"\'%;()&+]', '', text)
```

### 3. Ограничение доступа

```python
# Декоратор для проверки админских прав
from functools import wraps

def admin_only(func):
    @wraps(func)
    async def wrapper(update, context):
        user_id = update.effective_user.id
        if user_id != int(ADMIN_ID):
            await update.message.reply_text("❌ У вас нет прав доступа")
            return
        return await func(update, context)
    return wrapper

@admin_only
async def admin_command(update, context):
    # Только для админов
    pass
```

## 💳 Безопасность платежей

### 1. Настройка YooKassa

**✅ Правильно:**
```python
# config.py
import os

PAYMENT_PROVIDER_TOKEN = os.getenv('PAYMENT_PROVIDER_TOKEN')
YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID')
YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY')

if not PAYMENT_PROVIDER_TOKEN:
    raise ValueError("PAYMENT_PROVIDER_TOKEN не установлен!")
```

**❌ Неправильно:**
```python
# НЕ ДЕЛАЙТЕ ТАК!
PAYMENT_PROVIDER_TOKEN = "381764678:LIVE:xxxxx"  # Хардкод токена
```

### 2. Валидация платежей

```python
# payments.py
async def validate_payment(payment_data):
    """Проверка легитимности платежа"""
    
    # 1. Проверка суммы
    expected_amount = get_product_price(payment_data['product_id'])
    if payment_data['amount'] != expected_amount:
        raise ValueError("Неверная сумма платежа")
    
    # 2. Проверка пользователя
    user = db.get_user(payment_data['user_id'])
    if not user:
        raise ValueError("Пользователь не найден")
    
    # 3. Проверка подписи (если доступна)
    # verify_signature(payment_data)
    
    return True
```

### 3. Обработка ошибок платежей

```python
# payments.py
import logging

logger = logging.getLogger(__name__)

async def process_payment(payment_data):
    try:
        # Обработка платежа
        result = await yookassa_api.create_payment(payment_data)
        
        # Логирование успеха (без чувствительных данных!)
        logger.info(f"Платеж создан: order_id={payment_data['order_id']}")
        
        return result
        
    except Exception as e:
        # Логирование ошибки (без токенов и ключей!)
        logger.error(f"Ошибка платежа: {type(e).__name__}")
        
        # НЕ отправляем пользователю детали ошибки
        raise ValueError("Не удалось обработать платеж. Попробуйте позже.")
```

## 🔒 Безопасность API

### 1. CORS настройка

```python
# render_api.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-frontend.vercel.app",  # Production
        "http://localhost:5173"  # Development
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### 2. Rate Limiting

```python
# render_api.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.get("/api/products")
@limiter.limit("60/minute")  # 60 запросов в минуту
async def get_products(request: Request):
    return {"products": [...]}
```

### 3. JWT аутентификация

```python
# auth.py
from jose import jwt
from datetime import datetime, timedelta

SECRET_KEY = os.getenv('API_SECRET_KEY')
ALGORITHM = "HS256"

def create_access_token(user_id: int):
    expire = datetime.utcnow() + timedelta(hours=24)
    to_encode = {"user_id": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.JWTError:
        return None
```

## 📊 Мониторинг и логирование

### 1. Настройка логирования

```python
# bot.py
import logging
from logging.handlers import RotatingFileHandler

# Создаем логгер
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Файловый хендлер с ротацией
file_handler = RotatingFileHandler(
    'bot.log',
    maxBytes=10*1024*1024,  # 10 MB
    backupCount=5
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)

logger.addHandler(file_handler)

# Логируем важные события
logger.info("Бот запущен")
logger.warning("Подозрительная активность")
logger.error("Критическая ошибка")
```

### 2. Что логировать

**✅ Логируем:**
- Запуск/остановка бота
- Регистрации пользователей
- Создание заказов
- Успешные платежи
- Ошибки и исключения
- Админские действия

**❌ НЕ логируем:**
- Токены и ключи API
- Пароли
- Полные номера карт
- Персональные данные в открытом виде

```python
# Правильно
logger.info(f"Пользователь {user_id} создал заказ #{order_id}")

# Неправильно
logger.info(f"Платеж: token={payment_token}, card={card_number}")
```

## 🔄 Обновление зависимостей

### Проверка уязвимостей

```bash
# Установка safety
pip install safety

# Проверка известных уязвимостей
safety check

# Проверка устаревших пакетов
pip list --outdated
```

### Обновление пакетов

```bash
# Обновить все пакеты
pip install --upgrade -r requirements.txt

# Обновить конкретный пакет
pip install --upgrade python-telegram-bot

# Создать новый requirements.txt
pip freeze > requirements.txt
```

### График обновлений

- **Критические уязвимости:** Немедленно
- **Важные обновления:** Еженедельно
- **Минорные обновления:** Ежемесячно
- **Мажорные версии:** После тестирования

## 🚨 План реагирования на инциденты

### При компрометации ключей API

1. **Немедленно:**
   - Отозвать скомпрометированные ключи
   - Сгенерировать новые ключи
   - Обновить `.env` на всех серверах
   - Перезапустить все сервисы

2. **В течение часа:**
   - Проверить логи на подозрительную активность
   - Уведомить пользователей (если нужно)
   - Оценить ущерб

3. **В течение 24 часов:**
   - Провести полный аудит безопасности
   - Устранить уязвимость
   - Задокументировать инцидент

### Контакты для экстренных случаев

```
Администратор: [Ваш Telegram]
Техподдержка YooKassa: support@yookassa.ru
Техподдержка Telegram: @BotSupport
```

## 📚 Дополнительные ресурсы

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)
- [Telegram Bot API Security](https://core.telegram.org/bots/api#authorizing-your-bot)
- [YooKassa Security](https://yookassa.ru/developers/payment-acceptance/security)

---

**🔐 Безопасность - это процесс, а не состояние. Регулярно проверяйте и обновляйте меры защиты!**
