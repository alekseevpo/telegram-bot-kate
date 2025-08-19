# 🚀 Деплой Kate Bot на Vercel + Render

## 📋 План деплоя

1. **Frontend (Vue.js)** → **Vercel** (бесплатно, быстро)
2. **Backend (FastAPI)** → **Render** (бесплатно, Python)
3. **Telegram Bot** → **Render** (уже работает)

## 🌐 Шаг 1: Деплой Frontend на Vercel

### 1.1 Подготовка проекта
```bash
# В папке web-admin
npm run build
```

### 1.2 Создание аккаунта Vercel
1. Перейдите на [vercel.com](https://vercel.com)
2. Войдите через GitHub
3. Нажмите "New Project"

### 1.3 Импорт проекта
1. Выберите ваш GitHub репозиторий `bot_kate`
2. Настройте проект:
   - **Framework Preset**: `Vue.js`
   - **Root Directory**: `web-admin`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`
   - **Install Command**: `npm install`

### 1.4 Переменные окружения
Добавьте в Vercel:
```
API_URL=https://your-render-api.onrender.com
```

### 1.5 Деплой
Нажмите "Deploy" и дождитесь завершения.

**✅ Frontend будет доступен на: `https://your-project.vercel.app`**

## 🐳 Шаг 2: Деплой API на Render

### 2.1 Подготовка файлов
Убедитесь, что у вас есть:
- `render_api.py` - API для Render
- `requirements_render.txt` - зависимости
- `database.py` - модуль базы данных
- `config.py` - конфигурация

### 2.2 Создание аккаунта Render
1. Перейдите на [render.com](https://render.com)
2. Войдите через GitHub
3. Нажмите "New +" → "Web Service"

### 2.3 Настройка сервиса
1. **Connect Repository**: выберите `bot_kate`
2. **Name**: `kate-bot-api`
3. **Environment**: `Python 3`
4. **Build Command**: `pip install -r requirements_render.txt`
5. **Start Command**: `python render_api.py`

### 2.4 Переменные окружения
Добавьте в Render:
```
BOT_TOKEN=ваш_токен_бота
ADMIN_ID=ваш_telegram_id
DATABASE_PATH=./bot_database.db
PORT=8000
```

### 2.5 Деплой
Нажмите "Create Web Service" и дождитесь завершения.

**✅ API будет доступен на: `https://kate-bot-api.onrender.com`**

## 🔗 Шаг 3: Связывание Frontend и Backend

### 3.1 Обновление API URL в Vercel
В настройках Vercel проекта обновите:
```
API_URL=https://kate-bot-api.onrender.com
```

### 3.2 Обновление CORS в API
В `render_api.py` обновите домен Vercel:
```python
allow_origins=[
    "https://your-project.vercel.app",  # Ваш Vercel домен
    "https://*.vercel.app",
    "http://localhost:3000",
]
```

### 3.3 Перезапуск API
В Render нажмите "Manual Deploy" → "Deploy latest commit"

## 🧪 Шаг 4: Тестирование

### 4.1 Проверка Frontend
- Откройте ваш Vercel домен
- Проверьте главную страницу
- Проверьте каталог продуктов

### 4.2 Проверка API
- Откройте `https://your-api.onrender.com/health`
- Должен вернуться статус "ok"

### 4.3 Проверка админки
- Перейдите на `/admin`
- Войдите с вашим ADMIN_ID
- Проверьте все функции

## 🔧 Шаг 5: Настройка домена (опционально)

### 5.1 Покупка домена
Купите домен (например, `katebot.com`)

### 5.2 Настройка DNS
```
A     @     76.76.19.19      # Vercel
CNAME  www   your-project.vercel.app
```

### 5.3 Настройка в Vercel
1. В настройках проекта → "Domains"
2. Добавьте ваш домен
3. Настройте DNS записи

## 📱 Шаг 6: Мобильная оптимизация

### 6.1 PWA настройка
Добавьте в `index.html`:
```html
<meta name="theme-color" content="#1976D2">
<link rel="manifest" href="/manifest.json">
```

### 6.2 Создание manifest.json
```json
{
  "name": "Kate Bot",
  "short_name": "KateBot",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#ffffff",
  "theme_color": "#1976D2"
}
```

## 🚀 Результат

После деплоя у вас будет:

✅ **Публичный сайт**: `https://your-project.vercel.app`  
✅ **API сервер**: `https://kate-bot-api.onrender.com`  
✅ **Telegram бот**: работает на Render  
✅ **Мобильная версия**: адаптивный дизайн  
✅ **SSL сертификаты**: везде включены  

## 💡 Полезные ссылки

- [Vercel Dashboard](https://vercel.com/dashboard)
- [Render Dashboard](https://dashboard.render.com)
- [Vercel CLI](https://vercel.com/docs/cli)
- [Render Documentation](https://render.com/docs)

## 🆘 Решение проблем

### Frontend не загружается
- Проверьте Build Command в Vercel
- Убедитесь, что `dist/` папка создается

### API не отвечает
- Проверьте Start Command в Render
- Убедитесь, что все зависимости установлены

### CORS ошибки
- Проверьте настройки CORS в `render_api.py`
- Убедитесь, что домен Vercel добавлен

---

**🎉 Готово! Ваш Kate Bot теперь работает в облаке!** 