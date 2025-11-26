from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import *
from database import Database

class UserHandlers:
    """Обработчики команд пользователей"""
    
    def __init__(self, database: Database, payment_handler=None):
        self.db = database
        self.payment_handler = payment_handler
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /start"""
        user = update.effective_user
        chat_id = update.effective_chat.id
        
        # Добавляем пользователя в базу
        self.db.add_user(
            user_id=user.id,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name
        )
        
        # Обновляем этап
        self.db.update_user_stage(user.id, 'gender_selection')
        
        # Приветственное сообщение
        welcome_text = f"""
🌟 **Добро пожаловать, {user.first_name}!**

Я бот-помощник, который поможет вам получить доступ к ценным материалам 
и узнать больше о нашем методе работы.

Для начала давайте познакомимся! Какого вы пола?
        """
        
        keyboard = [
            [
                InlineKeyboardButton("👨 Мужчина", callback_data="gender_male"),
                InlineKeyboardButton("👩 Женщина", callback_data="gender_female")
            ],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        await self.show_main_menu(update.effective_chat.id, context)
    
    async def show_main_menu(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Показать главное меню"""
        menu_text = """
🤖 **Kate Bot - Ваш помощник!**

Выберите, что хотите сделать:
        """
        
        keyboard = [
            [InlineKeyboardButton("💎 Продукты", callback_data="main_shop")],
            [InlineKeyboardButton("📚 Бесплатные материалы", callback_data="main_materials")],
            [InlineKeyboardButton("📋 Мои заказы", callback_data="main_orders")],
            [InlineKeyboardButton("👤 Мой профиль", callback_data="main_profile")],
            [InlineKeyboardButton("🌐 Веб-сайт", url="https://telegram-bot-kate.vercel.app")],
            [InlineKeyboardButton("❓ Помощь", callback_data="main_help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=menu_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user_id = update.effective_user.id
        message_text = update.message.text
        chat_id = update.effective_chat.id
        
        # Получаем данные пользователя
        user_data = self.db.get_user(user_id)
        if not user_data:
            await self.start_command(update, context)
            return
        
        current_stage = user_data.get('stage', 'start')
        
        if current_stage == 'name_input':
            # Пользователь вводит имя
            self.db.update_user_data(user_id, 'name', message_text)
            self.db.update_user_stage(user_id, 'phone_input')  # Меняем этап на phone_input
            await self.send_free_materials(chat_id, context, message_text)
            
        elif current_stage == 'phone_input':
            # Пользователь вводит телефон
            self.db.update_user_data(user_id, 'phone', message_text)
            self.db.update_user_stage(user_id, 'phone_confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            user_name = updated_user_data.get('name', 'пользователь')
            
            confirmation_text = f"""
📋 **Проверьте ваши данные:**

👤 Имя: {user_name}
📱 Телефон: {message_text}

Все верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Все верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif current_stage == 'phone_confirmation':
            # Если пользователь что-то пишет на этапе подтверждения
            await update.message.reply_text(
                "⚠️ Пожалуйста, используйте кнопки выше для подтверждения или изменения данных."
            )
        
        elif current_stage == 'edit_name':
            # Редактирование имени
            self.db.update_user_data(user_id, 'name', message_text)
            self.db.update_user_stage(user_id, 'phone_confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            phone = updated_user_data.get('phone', 'Не указан')
            
            confirmation_text = f"""
✅ **Имя обновлено!**

📋 **Ваши данные:**

👤 Имя: {message_text}
📱 Телефон: {phone}

Все верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Все верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif current_stage == 'edit_phone':
            # Редактирование телефона
            self.db.update_user_data(user_id, 'phone', message_text)
            self.db.update_user_stage(user_id, 'phone_confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            name = updated_user_data.get('name', 'пользователь')
            
            confirmation_text = f"""
✅ **Телефон обновлен!**

📋 **Ваши данные:**

👤 Имя: {name}
📱 Телефон: {message_text}

Все верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Все верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка callback запросов"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        chat_id = query.message.chat_id
        data = query.data
        
        if data.startswith('gender_'):
            # Обработка выбора пола
            gender = 'male' if data == 'gender_male' else 'female'
            self.db.update_user_data(user_id, 'gender', gender)
            self.db.update_user_stage(user_id, 'name_input')
            await self.ask_for_name(chat_id, context)
            
        elif data.startswith('product_'):
            # Обработка выбора продукта
            product_id = data.split('_')[1]
            await self.handle_product_selection(chat_id, context, product_id, user_id)
            
        elif data == 'main_menu':
            # Показать главное меню
            await self.show_main_menu(chat_id, context)
            
        elif data == 'main_shop':
            # Показать продукты
            await self.shop_command(update, context)
            
        elif data == 'main_materials':
            # Показать бесплатные материалы
            user_data = self.db.get_user(user_id)
            if user_data and user_data.get('name'):
                await self.send_free_materials(chat_id, context, user_data['name'])
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="❌ Сначала нужно пройти регистрацию. Используйте /start"
                )
            
        elif data == 'main_orders':
            # Показать заказы пользователя
            orders = self.db.get_user_orders(user_id)
            if orders:
                orders_text = "📋 **Ваши заказы:**\n\n"
                for order in orders:
                    orders_text += f"🆔 Заказ #{order['id']}\n"
                    orders_text += f"📅 Дата: {order['order_date']}\n"
                    orders_text += f"💰 Сумма: {order['total_amount']} руб.\n"
                    orders_text += f"📊 Статус: {order['status']}\n\n"
            else:
                orders_text = "📋 У вас пока нет заказов."
            
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=orders_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        elif data == 'main_profile':
            # Показать профиль пользователя
            user_data = self.db.get_user(user_id)
            if user_data:
                profile_text = f"""
👤 **Ваш профиль:**

🆔 ID: `{user_data['user_id']}`
👤 Имя: {user_data.get('name', 'Не указано')}
👥 Пол: {user_data.get('gender', 'Не указан')}
📱 Телефон: {user_data.get('phone', 'Не указан')}
📊 Этап: {user_data.get('stage', 'Не указан')}
📅 Регистрация: {user_data.get('registration_date', 'Не указана')}
                """
            else:
                profile_text = "❌ Профиль не найден."
            
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=profile_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
        elif data == 'main_help':
            # Показать справку
            help_text = """
❓ **Справка по Kate Bot:**

🤖 **Основные функции:**
• Регистрация и знакомство
• Бесплатные материалы
• Продукты и услуги
• Личный кабинет
• Веб-версия сайта

📱 **Как использовать:**
• Используйте кнопки для навигации
• Всегда можно вернуться в главное меню
• Для покупок выберите "Продукты"
• Вопросы? Напишите администратору

🌐 **Веб-сайт:** https://telegram-bot-kate.vercel.app
            """
            
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=help_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif data == 'confirm_registration':
            # Подтверждение регистрации
            self.db.update_user_stage(user_id, 'registered')
            
            user_data = self.db.get_user(user_id)
            user_name = user_data.get('name', 'пользователь')
            phone = user_data.get('phone', 'Не указан')
            
            success_text = f"""
✅ **{user_name}, спасибо за регистрацию!**

Ваши данные успешно сохранены:
👤 Имя: {user_name}
📱 Телефон: {phone}

🎉 Теперь у вас есть полный доступ ко всем функциям бота!

📚 Вы можете:
• Изучить бесплатные материалы
• Посмотреть каталог услуг и продуктов
• Записаться на диагностический созвон
• Посетить наш веб-сайт

Используйте главное меню для навигации. Я всегда рад помочь! 💜
            """
            
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=success_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif data == 'edit_registration':
            # Выбор что редактировать
            edit_text = """
✏️ **Что вы хотите изменить?**
            """
            
            keyboard = [
                [InlineKeyboardButton("👤 Изменить имя", callback_data="edit_name")],
                [InlineKeyboardButton("📱 Изменить телефон", callback_data="edit_phone")],
                [InlineKeyboardButton("◀️ Назад", callback_data="back_to_confirmation")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=edit_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif data == 'edit_name':
            # Запрос нового имени
            self.db.update_user_stage(user_id, 'edit_name')
            
            await context.bot.send_message(
                chat_id=chat_id,
                text="👤 **Введите ваше новое имя:**"
            )
        
        elif data == 'edit_phone':
            # Запрос нового телефона
            self.db.update_user_stage(user_id, 'edit_phone')
            
            await context.bot.send_message(
                chat_id=chat_id,
                text="📱 **Введите ваш новый номер телефона:**"
            )
        
        elif data == 'back_to_confirmation':
            # Возврат к экрану подтверждения
            user_data = self.db.get_user(user_id)
            user_name = user_data.get('name', 'пользователь')
            phone = user_data.get('phone', 'Не указан')
            
            confirmation_text = f"""
📋 **Проверьте ваши данные:**

👤 Имя: {user_name}
📱 Телефон: {phone}

Все верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Все верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def ask_for_name(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Запрос имени пользователя"""
        name_text = """
Отлично! Теперь, пожалуйста, введите ваше имя:
        """
        
        await context.bot.send_message(chat_id=chat_id, text=name_text)
    
    async def send_free_materials(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_name: str):
        """Отправка бесплатных материалов"""
        materials_text = f"""
{user_name}, спасибо! 

{FREE_MATERIALS['welcome_message']}

Нажмите на кнопки ниже, чтобы открыть материалы:
        """
        
        # Создаем кнопки со ссылками на материалы
        keyboard = []
        for material in FREE_MATERIALS['materials']:
            keyboard.append([InlineKeyboardButton(
                material['title'],
                url=material['url']
            )])
        
        # Добавляем кнопку с анонимным опросом
        keyboard.append([InlineKeyboardButton(
            "📝 Анонимный опрос",
            url=ANONYMOUS_QUESTION_LINK
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=materials_text,
            reply_markup=reply_markup
        )
        
        # Отправляем отдельное сообщение с просьбой указать телефон
        phone_text = """
Теперь давайте договоримся о бесплатном диагностическом созвоне!

📞 Пожалуйста, оставьте ваш номер телефона для связи:
        """
        
        await context.bot.send_message(chat_id=chat_id, text=phone_text)
    
    async def send_products_menu(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_name: str):
        """Отправка меню продуктов"""
        products = self.db.get_products()
        
        if not products:
            # Добавляем базовые продукты
            self.db.add_product("Базовый курс", 5000, "Полный курс по основам метода")
            self.db.add_product("Продвинутый курс", 10000, "Углубленное изучение продвинутых техник")
            products = self.db.get_products()
        
        products_text = f"""
{user_name}, отлично! Теперь давайте посмотрим на наши платные продукты:

"""
        
        keyboard = []
        for product in products:
            products_text += f"""
💎 {product['name']}
💰 Цена: {product['price']} руб.
📝 {product['description']}

"""
            keyboard.append([InlineKeyboardButton(
                f"Купить {product['name']} - {product['price']} руб.",
                callback_data=f"product_{product['id']}"
            )])
        
        products_text += "\nВыберите продукт для покупки:"
        
        # Добавляем кнопку веб-версии и главное меню
        keyboard.append([InlineKeyboardButton(
            "🌐 Открыть веб-сайт", 
            url="https://telegram-bot-kate.vercel.app"
        )])
        keyboard.append([InlineKeyboardButton(
            "🏠 Главное меню", 
            callback_data="main_menu"
        )])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=products_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def handle_product_selection(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, product_id: str, user_id: int):
        """Обработка выбора продукта"""
        products = self.db.get_products()
        selected_product = None
        
        for product in products:
            if str(product['id']) == product_id:
                selected_product = product
                break
        
        if not selected_product:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Продукт не найден."
            )
            return
        
        # Если есть обработчик платежей - используем его
        if self.payment_handler:
            # Создаем временный update объект для payment_handler
            class FakeMessage:
                def __init__(self, chat_id):
                    self.chat_id = chat_id
                    self.chat = type('obj', (object,), {'id': chat_id})
            
            class FakeUpdate:
                def __init__(self, chat_id):
                    self.effective_chat = type('obj', (object,), {'id': chat_id})
                    self.message = FakeMessage(chat_id)
            
            fake_update = FakeUpdate(chat_id)
            await self.payment_handler.send_invoice(fake_update, context, int(product_id))
        else:
            # Если платежей нет - показываем информацию для связи с админом
            payment_text = f"""
💳 Оформление заказа

Продукт: {selected_product['name']}
Цена: {selected_product['price']} руб.

Для завершения покупки свяжитесь с администратором:
📧 Email: admin@example.com
📱 Telegram: @admin_username

Или используйте команду /admin для связи.
            """
            
            await context.bot.send_message(chat_id=chat_id, text=payment_text)
    
    async def shop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать каталог продуктов"""
        chat_id = update.effective_chat.id
        
        # Получаем продукты из базы
        products = self.db.get_products()
        
        if not products:
            # Добавляем базовые продукты, если их нет
            self.db.add_product("Базовый курс", 5000, "Полный курс по основам метода работы с кризисными ситуациями")
            self.db.add_product("Продвинутый курс", 10000, "Углубленное изучение продвинутых техник психологической помощи")
            self.db.add_product("Индивидуальная консультация", 3000, "Персональная консультация 60 минут")
            products = self.db.get_products()
        
        # Формируем текст каталога
        catalog_text = """
💎 **Каталог продуктов и услуг**

Выберите продукт для покупки:

"""
        
        keyboard = []
        for product in products:
            catalog_text += f"""
📦 **{product['name']}**
💰 {product['price']} руб.
📝 {product['description']}

"""
            # Добавляем кнопку для каждого продукта
            keyboard.append([InlineKeyboardButton(
                f"💳 {product['name']} - {product['price']} руб.",
                callback_data=f"product_{product['id']}"
            )])
        
        # Добавляем дополнительные кнопки
        keyboard.append([InlineKeyboardButton("🌐 Веб-сайт", url="https://telegram-bot-kate.vercel.app")])
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=catalog_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def cart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать корзину"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        # Корзина пока не реализована, показываем заказы
        cart_text = "🛒 **Корзина**\n\nФункция корзины временно недоступна.\nВы можете купить продукты напрямую из каталога."
        
        keyboard = [
            [InlineKeyboardButton("💎 В каталог", callback_data="main_shop")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=cart_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    
    async def add_to_cart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Добавить товар в корзину"""
        chat_id = update.effective_chat.id
        
        await context.bot.send_message(
            chat_id=chat_id,
            text="🛒 Функция корзины временно недоступна.\n\n💎 Перейдите в каталог и покупайте продукты напрямую!"
        )


class AdminHandlers:
    """Обработчики админ-команд"""
    
    def __init__(self, database: Database):
        self.db = database
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /admin"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ У вас нет доступа к админ-панели."
            )
            return
        
        # Админ-панель
        admin_text = """
🔧 Админ-панель

Выберите действие:
        """
        
        keyboard = [
            [InlineKeyboardButton("📊 Статистика", callback_data="admin_stats")],
            [InlineKeyboardButton("👥 Список пользователей", callback_data="admin_users")],
            [InlineKeyboardButton("🎯 Приглашение на встречу", callback_data="admin_meeting")],
            [InlineKeyboardButton("🔥 Специальное предложение", callback_data="admin_offer")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=admin_text,
            reply_markup=reply_markup
        )
    
    async def meeting_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Создание приглашения на встречу"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ У вас нет доступа к этой команде."
            )
            return
        
        if not context.args:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Использование: /meeting <название> | <описание> | <дата> | [ссылка]"
            )
            return
        
        # Разбираем параметры
        full_text = " ".join(context.args)
        parts = full_text.split("|")
        
        if len(parts) < 3:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Недостаточно параметров. Используйте: /meeting <название> | <описание> | <дата> | [ссылка]"
            )
            return
        
        title = parts[0].strip()
        description = parts[1].strip()
        date = parts[2].strip()
        link = parts[3].strip() if len(parts) > 3 else None
        
        # Отправляем приглашение
        success = await self.send_meeting_invitation(context, title, description, date, link)
        
        if success:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"✅ Приглашение на встречу '{title}' успешно отправлено!"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Ошибка при отправке приглашения."
            )
    
    async def offer_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Создание специального предложения"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ У вас нет доступа к этой команде."
            )
            return
        
        if not context.args:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Использование: /offer <название> | <описание> | [скидка] | [действует до]"
            )
            return
        
        # Разбираем параметры
        full_text = " ".join(context.args)
        parts = full_text.split("|")
        
        if len(parts) < 2:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Недостаточно параметров. Используйте: /offer <название> | <описание> | [скидка] | [действует до]"
            )
            return
        
        title = parts[0].strip()
        description = parts[1].strip()
        discount = parts[2].strip() if len(parts) > 2 else None
        valid_until = parts[3].strip() if len(parts) > 3 else None
        
        # Отправляем предложение
        success = await self.send_special_offer(context, title, description, discount, valid_until)
        
        if success:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"✅ Специальное предложение '{title}' успешно отправлено!"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="❌ Ошибка при отправке предложения."
            )
    
    async def send_meeting_invitation(self, context, title: str, description: str, date: str, link: str = None):
        """Отправка приглашения на встречу"""
        try:
            invitation_text = f"""
🎯 Приглашение на встречу

📅 {title}
📝 {description}
🕐 Дата: {date}

"""
            
            if link:
                invitation_text += f"🔗 Ссылка: {link}\n"
            
            invitation_text += """
Для участия свяжитесь с администратором или используйте команду /admin
            """
            
            # Отправляем всем пользователям
            users = self.db.get_all_users()
            sent_count = 0
            
            for user in users:
                try:
                    await context.bot.send_message(
                        chat_id=user['user_id'],
                        text=invitation_text
                    )
                    sent_count += 1
                except:
                    continue
            
            return sent_count > 0
            
        except Exception as e:
            print(f"Ошибка при отправке приглашения: {e}")
            return False
    
    async def send_special_offer(self, context, title: str, description: str, discount: str = None, valid_until: str = None):
        """Отправка специального предложения"""
        try:
            offer_text = f"""
🔥 Специальное предложение!

{title}

📝 {description}

"""
            
            if discount:
                offer_text += f"💰 Скидка: {discount}\n"
            
            if valid_until:
                offer_text += f"⏰ Действует до: {valid_until}\n"
            
            offer_text += """
Для получения предложения используйте команду /start
            """
            
            # Отправляем всем пользователям
            users = self.db.get_all_users()
            sent_count = 0
            
            for user in users:
                try:
                    await context.bot.send_message(
                        chat_id=user['user_id'],
                        text=offer_text
                    )
                    sent_count += 1
                except:
                    continue
            
            return sent_count > 0
            
        except Exception as e:
            print(f"Ошибка при отправке предложения: {e}")
            return False 