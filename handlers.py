from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import *
from database import Database

class UserHandlers:
    """Обработчики команд пользователей"""
    
    def __init__(self, database: Database):
        self.db = database
    
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
🌟 Добро пожаловать, {user.first_name}!

Я бот-помощник, который поможет вам получить доступ к ценным материалам 
и узнать больше о нашем методе работы.

Для начала давайте познакомимся! Какого вы пола?
        """
        
        keyboard = [
            [
                InlineKeyboardButton("👨 Мужчина", callback_data="gender_male"),
                InlineKeyboardButton("👩 Женщина", callback_data="gender_female")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=welcome_text,
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        help_text = """
🤖 Доступные команды:

/start - Начать работу с ботом
/help - Показать эту справку

Если у вас есть вопросы, используйте команду /start для начала работы.
        """
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=help_text
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
            self.db.update_user_stage(user_id, 'free_materials')
            await self.send_free_materials(chat_id, context, message_text)
            
        elif current_stage == 'phone_input':
            # Пользователь вводит телефон
            self.db.update_user_data(user_id, 'phone', message_text)
            self.db.update_user_stage(user_id, 'products')
            await self.send_products_menu(chat_id, context, user_data.get('name', 'пользователь'))
    
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
"""
        
        for material in FREE_MATERIALS['materials']:
            materials_text += f"\n{material}"
        
        materials_text += f"""

🔗 Ссылка на анонимный вопрос:
{ANONYMOUS_QUESTION_LINK}

Теперь давайте договоримся о бесплатном диагностическом созвоне!

📞 Пожалуйста, оставьте ваш номер телефона для связи:
        """
        
        await context.bot.send_message(chat_id=chat_id, text=materials_text)
    
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
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=products_text,
            reply_markup=reply_markup
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
        
        # Информация о покупке
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