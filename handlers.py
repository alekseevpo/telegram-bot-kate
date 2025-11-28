import logging
import re
import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from config import *
from database import Database

logger = logging.getLogger(__name__)

class UserHandlers:
    """Обработчики команд пользователей"""
    
    def __init__(self, database: Database, payment_handler=None):
        self.db = database
        self.payment_handler = payment_handler
    
    def validate_phone_number(self, phone: str) -> bool:
        """
        Валидация номера телефона
        
        Принимаются форматы:
        - 89117929394 (11 цифр, начинается с 8)
        - 79117929394 (11 цифр, начинается с 7)
        - +79117929394 (+ и 11 цифр, начинается с 7)
        - С пробелами, скобками, дефисами: +7 (911) 792-93-94
        
        Returns:
            bool: True если номер корректный, False если нет
        """
        # Убираем все символы кроме цифр и +
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Проверяем различные форматы
        patterns = [
            r'^8\d{10}$',      # 8 + 10 цифр
            r'^7\d{10}$',      # 7 + 10 цифр
            r'^\+7\d{10}$',    # +7 + 10 цифр
        ]
        
        for pattern in patterns:
            if re.match(pattern, cleaned):
                return True
        
        return False
    
    async def send_or_edit_message(
        self, 
        context: ContextTypes.DEFAULT_TYPE,
        chat_id: int,
        user_id: int,
        text: str,
        reply_markup=None,
        parse_mode='Markdown',
        query=None
    ):
        """
        Умная отправка сообщений: удаляет старое и отправляет новое (эффект замены)
        
        Args:
            context: Контекст бота
            chat_id: ID чата
            user_id: ID пользователя
            text: Текст сообщения
            reply_markup: Клавиатура
            parse_mode: Режим парсинга (Markdown/HTML)
            query: CallbackQuery (если есть, удаляет его сообщение)
        """
        try:
            # Определяем ID сообщения для удаления
            message_to_delete = None
            
            if query and query.message:
                # Если есть query, удаляем его сообщение
                message_to_delete = query.message.message_id
                logger.info(f"🗑️ Планируется удаление сообщения из query: {message_to_delete}")
            else:
                # Иначе берем последнее сохраненное
                message_to_delete = self.db.get_last_message_id(user_id)
                logger.info(f"🗑️ Планируется удаление последнего сохраненного сообщения: {message_to_delete}")
            
            # Удаляем старое сообщение
            if message_to_delete:
                try:
                    await context.bot.delete_message(
                        chat_id=chat_id,
                        message_id=message_to_delete
                    )
                    logger.info(f"✅ Удалено сообщение {message_to_delete}")
                except Exception as e:
                    logger.warning(f"❌ Не удалось удалить сообщение {message_to_delete}: {e}")
            else:
                logger.info("⚠️ Нет сообщения для удаления")
            
            # Отправляем новое сообщение
            sent_message = await context.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=reply_markup,
                parse_mode=parse_mode
            )
            
            # Сохраняем ID нового сообщения
            self.db.update_last_message_id(user_id, sent_message.message_id)
            logger.info(f"📨 Отправлено новое сообщение {sent_message.message_id}")
            return sent_message.message_id
            
        except Exception as e:
            logger.error(f"❌ Ошибка при отправке/удалении сообщения: {e}")
            return None
    
    async def delete_user_message(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int, message_id: int):
        """Удаление сообщения пользователя"""
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        except Exception as e:
            logger.warning(f"Не удалось удалить сообщение пользователя: {e}")
    
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
        
        # Проверяем, зарегистрирован ли пользователь
        user_data = self.db.get_user(user.id)
        is_registered = (
            user_data and 
            user_data.get('name') and 
            user_data.get('phone') and
            user_data.get('stage') == 'registered'
        )
        
        if is_registered:
            # Если пользователь уже зарегистрирован, показываем главное меню
            logger.info(f"Пользователь {user.id} уже зарегистрирован, показываем главное меню")
            await self.show_main_menu(chat_id, user.id, context)
        else:
            # Обновляем этап только для новых/незарегистрированных пользователей
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
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            sent_message = await context.bot.send_message(
                chat_id=chat_id,
                text=welcome_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # Сохраняем ID приветственного сообщения для последующего удаления
            self.db.update_last_message_id(user.id, sent_message.message_id)
            logger.info(f"📨 Отправлено приветственное сообщение {sent_message.message_id}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка команды /help"""
        await self.show_main_menu(update.effective_chat.id, update.effective_user.id, context)
    
    async def show_main_menu(self, chat_id: int, user_id: int, context: ContextTypes.DEFAULT_TYPE, query=None):
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
        
        await self.send_or_edit_message(
            context=context,
            chat_id=chat_id,
            user_id=user_id,
            text=menu_text,
            reply_markup=reply_markup,
            parse_mode='Markdown',
            query=query
        )
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка текстовых сообщений"""
        user_id = update.effective_user.id
        message_text = update.message.text
        chat_id = update.effective_chat.id
        message_id = update.message.message_id
        
        # Получаем данные пользователя
        user_data = self.db.get_user(user_id)
        if not user_data:
            await self.start_command(update, context)
            return
        
        current_stage = user_data.get('stage', 'start')
        
        # Удаляем сообщение пользователя для чистоты чата (кроме stage='phone_confirmation')
        if current_stage != 'phone_confirmation':
            await self.delete_user_message(context, chat_id, message_id)
        
        if current_stage == 'name_input':
            # Пользователь вводит имя
            logger.info(f"Получено имя от user_id={user_id}: {message_text}")
            self.db.update_user_data(user_id, 'name', message_text)
            self.db.update_user_stage(user_id, 'phone_input')
            logger.info(f"Обновлен stage на 'phone_input' для user_id={user_id}")
            
            # Приятное приветствие и просьба указать телефон
            phone_text = f"""
Приятно познакомиться, {message_text}! 😊

Для завершения регистрации, пожалуйста, укажите ваш номер телефона.

📞 Формат: +7 (911) 792-93-94

После подтверждения данных вы получите доступ к бесплатным материалам!
            """
            
            # Используем send_or_edit_message для удаления предыдущих сообщений
            logger.info(f"Отправляем просьбу указать телефон для user_id={user_id}")
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=phone_text
            )
            logger.info(f"✅ Просьба указать телефон отправлена")
            
        elif current_stage == 'phone_input':
            # Пользователь вводит телефон
            logger.info(f"Получен телефон от user_id={user_id}: {message_text}")
            
            # Валидация номера телефона
            if not self.validate_phone_number(message_text):
                logger.warning(f"Некорректный номер телефона от user_id={user_id}: {message_text}")
                
                error_text = """
❌ **Некорректный номер телефона**

Пожалуйста, введите номер в правильном формате.

📞 **Примеры корректных форматов:**

• `89117929394` (8 + 10 цифр)
• `79117929394` (7 + 10 цифр)  
• `+79117929394` (+7 + 10 цифр)
• `+7 (911) 792-93-94` (с пробелами и скобками)
• `8 911 792-93-94` (с пробелами и дефисами)

Попробуйте ещё раз:
                """
                
                await self.send_or_edit_message(
                    context=context,
                    chat_id=chat_id,
                    user_id=user_id,
                    text=error_text,
                    parse_mode='Markdown'
                )
                return
            
            # Номер валидный - сохраняем и переходим к подтверждению
            logger.info(f"✅ Номер телефона валидный для user_id={user_id}")
            self.db.update_user_data(user_id, 'phone', message_text)
            self.db.update_user_stage(user_id, 'phone_confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            user_name = updated_user_data.get('name', 'пользователь')
            gender = updated_user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            confirmation_text = f"""
✅ **Благодарим за регистрацию!**

Пожалуйста, подтвердите введенные данные:

👥 Пол: {gender_text}
👤 Имя: {user_name}
📱 Телефон: {message_text}

Всё верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Всё верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Подтверждение отправлено")
        
        elif current_stage == 'confirmation':
            # Если пользователь что-то пишет на этапе подтверждения
            await update.message.reply_text(
                "⚠️ Пожалуйста, используйте кнопки выше для подтверждения или изменения данных."
            )
        
        elif current_stage == 'phone_confirmation':
            # Если пользователь что-то пишет на этапе подтверждения (старая версия)
            await update.message.reply_text(
                "⚠️ Пожалуйста, используйте кнопки выше для подтверждения или изменения данных."
            )
        
        elif current_stage == 'edit_profile_name':
            # Ввод имени при редактировании профиля
            logger.info(f"Получено имя при редактировании профиля от user_id={user_id}: {message_text}")
            self.db.update_user_data(user_id, 'name', message_text)
            self.db.update_user_stage(user_id, 'edit_profile_phone')
            
            # Просьба указать телефон
            phone_text = f"""
Приятно познакомиться, {message_text}! 😊

Для завершения редактирования профиля, пожалуйста, укажите ваш номер телефона.

📞 Формат: +7 (911) 792-93-94
            """
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=phone_text
            )
            logger.info(f"✅ Просьба указать телефон при редактировании отправлена")
        
        elif current_stage == 'edit_profile_phone':
            # Ввод телефона при редактировании профиля
            logger.info(f"Получен телефон при редактировании профиля от user_id={user_id}: {message_text}")
            
            # Валидация номера телефона
            if not self.validate_phone_number(message_text):
                logger.warning(f"Некорректный номер телефона при редактировании профиля от user_id={user_id}")
                
                error_text = """
❌ **Некорректный номер телефона**

Пожалуйста, введите номер в правильном формате.

📞 **Примеры корректных форматов:**

• `89117929394` (8 + 10 цифр)
• `79117929394` (7 + 10 цифр)  
• `+79117929394` (+7 + 10 цифр)
• `+7 (911) 792-93-94` (с пробелами и скобками)
• `8 911 792-93-94` (с пробелами и дефисами)

Попробуйте ещё раз:
                """
                
                await self.send_or_edit_message(
                    context=context,
                    chat_id=chat_id,
                    user_id=user_id,
                    text=error_text,
                    parse_mode='Markdown'
                )
                return
            
            # Номер валидный - сохраняем и переходим к подтверждению
            logger.info(f"✅ Номер телефона валидный при редактировании профиля для user_id={user_id}")
            self.db.update_user_data(user_id, 'phone', message_text)
            self.db.update_user_stage(user_id, 'edit_profile_confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            user_name = updated_user_data.get('name', 'пользователь')
            gender = updated_user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            confirmation_text = f"""
✅ **Профиль обновлен!**

Пожалуйста, подтвердите введенные данные:

👥 Пол: {gender_text}
👤 Имя: {user_name}
📱 Телефон: {message_text}

Всё верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Всё верно", callback_data="confirm_profile_edit"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_profile")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            logger.info(f"✅ Подтверждение редактирования профиля отправлено")
        
        elif current_stage == 'edit_profile_confirmation':
            # Если пользователь что-то пишет на этапе подтверждения редактирования
            await update.message.reply_text(
                "⚠️ Пожалуйста, используйте кнопки выше для подтверждения или изменения данных."
            )
        
        elif current_stage == 'edit_name_simple':
            # Редактирование имени (упрощенная регистрация)
            self.db.update_user_data(user_id, 'name', message_text)
            self.db.update_user_stage(user_id, 'confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            gender = updated_user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            confirmation_text = f"""
✅ **Имя обновлено!**

Пожалуйста, подтвердите введенные данные:

👥 Пол: {gender_text}
👤 Имя: {message_text}

Всё верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Всё верно", callback_data="confirm_simple_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_simple_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif current_stage == 'edit_name':
            # Редактирование имени
            self.db.update_user_data(user_id, 'name', message_text)
            self.db.update_user_stage(user_id, 'phone_confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            phone = updated_user_data.get('phone', 'Не указан')
            gender = updated_user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            confirmation_text = f"""
✅ **Имя обновлено!**

Пожалуйста, подтвердите введенные данные:

👥 Пол: {gender_text}
👤 Имя: {message_text}
📱 Телефон: {phone}

Всё верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Всё верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
        
        elif current_stage == 'edit_phone':
            # Редактирование телефона
            logger.info(f"Редактирование телефона от user_id={user_id}: {message_text}")
            
            # Валидация номера телефона
            if not self.validate_phone_number(message_text):
                logger.warning(f"Некорректный номер телефона при редактировании от user_id={user_id}")
                
                error_text = """
❌ **Некорректный номер телефона**

Пожалуйста, введите номер в правильном формате.

📞 **Примеры корректных форматов:**

• `89117929394` (8 + 10 цифр)
• `79117929394` (7 + 10 цифр)  
• `+79117929394` (+7 + 10 цифр)
• `+7 (911) 792-93-94` (с пробелами и скобками)
• `8 911 792-93-94` (с пробелами и дефисами)

Попробуйте ещё раз:
                """
                
                await self.send_or_edit_message(
                    context=context,
                    chat_id=chat_id,
                    user_id=user_id,
                    text=error_text,
                    parse_mode='Markdown'
                )
                return
            
            # Номер валидный - обновляем
            logger.info(f"✅ Номер телефона валидный при редактировании для user_id={user_id}")
            self.db.update_user_data(user_id, 'phone', message_text)
            self.db.update_user_stage(user_id, 'phone_confirmation')
            
            # Получаем обновленные данные из БД
            updated_user_data = self.db.get_user(user_id)
            name = updated_user_data.get('name', 'пользователь')
            gender = updated_user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            confirmation_text = f"""
✅ **Телефон обновлен!**

Пожалуйста, подтвердите введенные данные:

👥 Пол: {gender_text}
👤 Имя: {name}
📱 Телефон: {message_text}

Всё верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Всё верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
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
            gender_text = 'мужчина' if gender == 'male' else 'женщина'
            
            self.db.update_user_data(user_id, 'gender', gender)
            self.db.update_user_stage(user_id, 'name_input')
            
            # Удаляем предыдущее сообщение и отправляем новое с просьбой ввести имя
            name_request_text = f"""
Отлично! Вы выбрали: {gender_text}

Теперь, пожалуйста, введите ваше имя:
            """
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=name_request_text,
                query=query
            )
            
        elif data.startswith('product_'):
            # Обработка выбора продукта - показываем описание
            product_id = data.split('_')[1]
            await self.show_product_details(chat_id, context, product_id, user_id, query=query)
        
        elif data.startswith('buy_product_'):
            # Обработка покупки продукта - переходим к оплате
            product_id = data.split('_')[2]
            await self.handle_product_purchase(chat_id, context, product_id, user_id)
        
        elif data.startswith('add_cart_'):
            # Добавление продукта в корзину
            product_id = int(data.split('_')[2])
            if self.db.add_to_cart(user_id, product_id):
                await query.answer("✅ Товар добавлен в корзину!", show_alert=False)
                # Обновляем описание продукта с новыми кнопками
                await self.show_product_details(chat_id, context, str(product_id), user_id, query=query)
            else:
                await query.answer("❌ Ошибка при добавлении в корзину", show_alert=True)
        
        elif data.startswith('remove_cart_'):
            # Удаление продукта из корзины
            product_id = int(data.split('_')[2])
            if self.db.remove_from_cart(user_id, product_id):
                await query.answer("✅ Товар удален из корзины", show_alert=False)
                # Обновляем описание продукта с новыми кнопками
                await self.show_product_details(chat_id, context, str(product_id), user_id, query=query)
            else:
                await query.answer("❌ Ошибка при удалении из корзины", show_alert=True)
        
        elif data.startswith('add_fav_'):
            # Добавление продукта в избранное
            product_id = int(data.split('_')[2])
            if self.db.add_to_favorites(user_id, product_id):
                await query.answer("❤️ Товар добавлен в избранное!", show_alert=False)
                # Обновляем описание продукта с новыми кнопками
                await self.show_product_details(chat_id, context, str(product_id), user_id, query=query)
            else:
                await query.answer("❌ Ошибка при добавлении в избранное", show_alert=True)
        
        elif data.startswith('remove_fav_'):
            # Удаление продукта из избранного
            product_id = int(data.split('_')[2])
            if self.db.remove_from_favorites(user_id, product_id):
                await query.answer("✅ Товар удален из избранного", show_alert=False)
                # Обновляем описание продукта с новыми кнопками
                await self.show_product_details(chat_id, context, str(product_id), user_id, query=query)
            else:
                await query.answer("❌ Ошибка при удалении из избранного", show_alert=True)
            
        elif data == 'main_menu':
            # Показать главное меню
            await self.show_main_menu(chat_id, user_id, context, query=query)
            
        elif data == 'main_shop':
            # Показать продукты
            await self.shop_command(update, context, query=query)
            
        elif data == 'main_materials':
            # Показать бесплатные материалы
            user_data = self.db.get_user(user_id)
            
            # Логирование для отладки
            logger.info(f"Запрос материалов от user_id={user_id}")
            logger.info(f"user_data: name={user_data.get('name')}, phone={user_data.get('phone')}, stage={user_data.get('stage')}")
            
            # Проверяем полную регистрацию: имя, телефон и stage='registered'
            is_registered = (
                user_data and 
                user_data.get('name') and 
                user_data.get('phone') and
                user_data.get('stage') == 'registered'
            )
            
            logger.info(f"is_registered={is_registered}")
            
            if is_registered:
                # Пользователь уже зарегистрирован - просто показываем материалы
                logger.info("Показываем материалы зарегистрированному пользователю из главного меню")
                await self.send_free_materials(chat_id, context, user_data['name'], is_registered=True, source='menu')
            else:
                # Пользователь НЕ зарегистрирован полностью - требуем завершить регистрацию
                logger.info(f"Требуем завершить регистрацию. Текущий stage: {user_data.get('stage')}")
                
                incomplete_text = """
❌ **Доступ к материалам закрыт**

Для получения бесплатных материалов необходимо завершить регистрацию.

📝 Это займет всего 1 минуту!

Нажмите кнопку ниже, чтобы продолжить:
                """
                
                keyboard = [[InlineKeyboardButton("📝 Завершить регистрацию", callback_data="start_registration")]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await self.send_or_edit_message(
                    context=context,
                    chat_id=chat_id,
                    user_id=user_id,
                    text=incomplete_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown',
                    query=query
                )
            
        elif data == 'main_orders':
            # Показать заказы пользователя
            await self.show_orders_menu(chat_id, context, user_id, query=query)
        
        elif data.startswith('order_details_'):
            # Показать детали заказа
            order_id = int(data.split('_')[2])
            await self.show_order_details(chat_id, context, user_id, order_id, query=query)
        
        elif data.startswith('pay_order_'):
            # Оплата заказа
            order_id = int(data.split('_')[2])
            await self.pay_order(chat_id, context, user_id, order_id)
        
        elif data == 'create_order_from_cart':
            # Создание заказа из корзины
            await self.create_order_from_cart(chat_id, context, user_id, query=query)
        
        elif data == 'clear_cart':
            # Очистка корзины
            if self.db.clear_cart(user_id):
                await query.answer("✅ Корзина очищена", show_alert=False) if query else None
                cart_text = """
🛒 **Корзина очищена**

Ваша корзина теперь пуста.
                """
                keyboard = [
                    [InlineKeyboardButton("💎 В каталог", callback_data="main_shop")],
                    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                await self.send_or_edit_message(
                    context=context,
                    chat_id=chat_id,
                    user_id=user_id,
                    text=cart_text,
                    reply_markup=reply_markup,
                    parse_mode='Markdown',
                    query=query
                )
            else:
                await query.answer("❌ Ошибка при очистке корзины", show_alert=True) if query else None
            
        elif data == 'main_profile':
            # Показать профиль пользователя
            user_data = self.db.get_user(user_id)
            if user_data:
                gender = user_data.get('gender', 'не указан')
                gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
                
                profile_text = f"""
👤 **Ваш профиль:**

🆔 ID: `{user_data['user_id']}`
👤 Имя: {user_data.get('name', 'Не указано')}
👥 Пол: {gender_text}
📱 Телефон: {user_data.get('phone', 'Не указан')}
📅 Регистрация: {user_data.get('registration_date', 'Не указана')}
                """
            else:
                profile_text = "❌ Профиль не найден."
            
            keyboard = [
                [InlineKeyboardButton("✏️ Редактировать профиль", callback_data="edit_profile")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=profile_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
        
        elif data == 'edit_profile':
            # Начало редактирования профиля (тот же порядок, что и при регистрации)
            logger.info(f"Начало редактирования профиля user_id={user_id}")
            
            # Устанавливаем stage для начала редактирования
            self.db.update_user_stage(user_id, 'edit_profile_gender')
            
            edit_start_text = """
✏️ **Редактирование профиля**

Давайте обновим ваши данные. Начнем с выбора пола:

Какого вы пола?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("👨 Мужчина", callback_data="edit_profile_gender_male"),
                    InlineKeyboardButton("👩 Женщина", callback_data="edit_profile_gender_female")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=edit_start_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
        
        elif data.startswith('edit_profile_gender_'):
            # Обработка выбора пола при редактировании профиля
            gender = 'male' if data == 'edit_profile_gender_male' else 'female'
            gender_text = 'мужчина' if gender == 'male' else 'женщина'
            
            self.db.update_user_data(user_id, 'gender', gender)
            self.db.update_user_stage(user_id, 'edit_profile_name')
            
            name_request_text = f"""
Отлично! Вы выбрали: {gender_text}

Теперь, пожалуйста, введите ваше имя:
            """
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=name_request_text,
                query=query
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
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=help_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
        
        elif data == 'confirm_simple_registration':
            # Подтверждение упрощенной регистрации (без телефона)
            logger.info(f"Подтверждение упрощенной регистрации user_id={user_id}")
            self.db.update_user_stage(user_id, 'registered')
            
            user_data = self.db.get_user(user_id)
            user_name = user_data.get('name', 'пользователь')
            
            logger.info(f"После update_user_stage: name={user_name}, stage={user_data.get('stage')}")
            
            success_text = f"""
✅ **{user_name}, отлично! Регистрация завершена!**

🎁 Сейчас вы получите доступ к бесплатным материалам...
            """
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=success_text,
                parse_mode='Markdown'
            )
            
            # Отправляем бесплатные материалы ПОСЛЕ регистрации
            logger.info(f"Отправка материалов с is_registered=True")
            await self.send_free_materials(chat_id, context, user_name, is_registered=True)
        
        elif data == 'edit_simple_registration':
            # Редактирование данных упрощенной регистрации
            edit_text = """
✏️ **Что вы хотите изменить?**
            """
            
            keyboard = [
                [InlineKeyboardButton("👥 Изменить пол", callback_data="edit_gender")],
                [InlineKeyboardButton("👤 Изменить имя", callback_data="edit_name_simple")],
                [InlineKeyboardButton("◀️ Назад", callback_data="back_to_simple_confirmation")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=edit_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
        
        elif data == 'edit_gender':
            # Запрос нового пола
            self.db.update_user_stage(user_id, 'gender_selection')
            
            gender_text = """
👥 **Выберите ваш пол:**
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("👨 Мужчина", callback_data="gender_male"),
                    InlineKeyboardButton("👩 Женщина", callback_data="gender_female")
                ],
                [InlineKeyboardButton("◀️ Назад", callback_data="back_to_simple_confirmation")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=gender_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
        
        elif data == 'edit_name_simple':
            # Запрос нового имени
            self.db.update_user_stage(user_id, 'edit_name_simple')
            
            await context.bot.send_message(
                chat_id=chat_id,
                text="👤 **Введите ваше новое имя:**",
                parse_mode='Markdown'
            )
        
        elif data == 'back_to_simple_confirmation':
            # Возврат к подтверждению
            user_data = self.db.get_user(user_id)
            user_name = user_data.get('name', 'пользователь')
            gender = user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            confirmation_text = f"""
✅ **Благодарим за регистрацию!**

Пожалуйста, подтвердите введенные данные:

👥 Пол: {gender_text}
👤 Имя: {user_name}

Всё верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Всё верно", callback_data="confirm_simple_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_simple_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            self.db.update_user_stage(user_id, 'confirmation')
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
        
        elif data == 'confirm_registration':
            # Подтверждение регистрации
            logger.info(f"Подтверждение регистрации user_id={user_id}")
            self.db.update_user_stage(user_id, 'registered')
            
            user_data = self.db.get_user(user_id)
            user_name = user_data.get('name', 'пользователь')
            phone = user_data.get('phone', 'Не указан')
            gender = user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            logger.info(f"После update_user_stage: name={user_name}, phone={phone}, gender={gender_text}, stage={user_data.get('stage')}")
            
            success_text = f"""
✅ **{user_name}, отлично! Регистрация завершена!**

Ваши данные:
👥 Пол: {gender_text}
👤 Имя: {user_name}
📱 Телефон: {phone}

🎁 Сейчас вы получите доступ к бесплатным материалам...
            """
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=success_text,
                parse_mode='Markdown'
            )
            
            # Отправляем бесплатные материалы ПОСЛЕ регистрации
            logger.info(f"Отправка материалов с is_registered=True")
            await self.send_free_materials(chat_id, context, user_name, is_registered=True)
        
        elif data == 'confirm_profile_edit':
            # Подтверждение редактирования профиля
            logger.info(f"Подтверждение редактирования профиля user_id={user_id}")
            self.db.update_user_stage(user_id, 'registered')
            
            user_data = self.db.get_user(user_id)
            user_name = user_data.get('name', 'пользователь')
            phone = user_data.get('phone', 'Не указан')
            gender = user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            success_text = f"""
✅ **{user_name}, профиль успешно обновлен!**

Ваши обновленные данные:
👥 Пол: {gender_text}
👤 Имя: {user_name}
📱 Телефон: {phone}

Изменения сохранены!
            """
            
            keyboard = [
                [InlineKeyboardButton("👤 Мой профиль", callback_data="main_profile")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=success_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
            logger.info(f"✅ Профиль обновлен для user_id={user_id}")
        
        elif data == 'edit_registration':
            # Выбор что редактировать
            edit_text = """
✏️ **Что вы хотите изменить?**
            """
            
            keyboard = [
                [InlineKeyboardButton("👥 Изменить пол", callback_data="edit_gender")],
                [InlineKeyboardButton("👤 Изменить имя", callback_data="edit_name")],
                [InlineKeyboardButton("📱 Изменить телефон", callback_data="edit_phone")],
                [InlineKeyboardButton("◀️ Назад", callback_data="back_to_confirmation")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=edit_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
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
        
        elif data == 'start_registration':
            # Начать регистрацию заново
            await self.start_command(update, context)
        
        elif data == 'back_to_confirmation':
            # Возврат к экрану подтверждения
            user_data = self.db.get_user(user_id)
            user_name = user_data.get('name', 'пользователь')
            phone = user_data.get('phone', 'Не указан')
            gender = user_data.get('gender', 'не указан')
            gender_text = 'Мужчина' if gender == 'male' else 'Женщина' if gender == 'female' else 'Не указан'
            
            confirmation_text = f"""
✅ **Благодарим за регистрацию!**

Пожалуйста, подтвердите введенные данные:

👥 Пол: {gender_text}
👤 Имя: {user_name}
📱 Телефон: {phone}

Всё верно?
            """
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Всё верно", callback_data="confirm_registration"),
                    InlineKeyboardButton("✏️ Изменить", callback_data="edit_registration")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            self.db.update_user_stage(user_id, 'phone_confirmation')
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
    
    async def ask_for_name(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE):
        """Запрос имени пользователя"""
        name_text = """
Отлично! Теперь, пожалуйста, введите ваше имя:
        """
        
        await context.bot.send_message(chat_id=chat_id, text=name_text)
    
    async def send_free_materials(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_name: str, is_registered: bool = False, source: str = 'registration'):
        """
        Отправка бесплатных материалов
        
        Args:
            chat_id: ID чата
            context: Контекст бота
            user_name: Имя пользователя
            is_registered: Зарегистрирован ли пользователь
            source: Источник запроса - 'registration' (после регистрации) или 'menu' (из главного меню)
        """
        # Разные тексты в зависимости от источника
        if source == 'registration':
            # Сообщение после регистрации
            materials_text = f"""
🎉 **{user_name}, поздравляем с завершением регистрации!**

{FREE_MATERIALS['welcome_message']}

🎁 Ниже вы найдете бесплатные материалы, которые помогут вам начать:

Нажмите на кнопки ниже, чтобы открыть материалы:
            """
        else:
            # Сообщение из главного меню
            materials_text = f"""
📚 **Бесплатные материалы**

{FREE_MATERIALS['welcome_message']}

Выберите материал, который вас интересует:
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
        
        # Если пользователь уже зарегистрирован, добавляем кнопку "Главное меню"
        if is_registered:
            keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=chat_id,
            text=materials_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
        
        # Просим телефон ТОЛЬКО если пользователь еще не зарегистрирован
        if not is_registered:
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
    
    async def show_product_details(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, product_id: str, user_id: int, query=None):
        """Показать описание продукта"""
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
        
        # Проверяем, есть ли продукт в корзине и избранном
        in_cart = self.db.is_in_cart(user_id, int(product_id))
        in_favorites = self.db.is_in_favorites(user_id, int(product_id))
        
        # Формируем описание продукта
        product_details = f"""
📦 **{selected_product['name']}**

💰 **Цена:** {selected_product['price']} руб.

📝 **Описание:**
{selected_product.get('description', 'Описание отсутствует')}

Выберите действие:
        """
        
        keyboard = []
        
        # Кнопка корзины
        if in_cart:
            keyboard.append([InlineKeyboardButton("🛒 Удалить из корзины", callback_data=f"remove_cart_{product_id}")])
        else:
            keyboard.append([InlineKeyboardButton("🛒 Добавить в корзину", callback_data=f"add_cart_{product_id}")])
        
        # Кнопка избранного
        if in_favorites:
            keyboard.append([InlineKeyboardButton("❤️ Удалить из избранного", callback_data=f"remove_fav_{product_id}")])
        else:
            keyboard.append([InlineKeyboardButton("🤍 Добавить в избранное", callback_data=f"add_fav_{product_id}")])
        
        # Кнопка покупки
        keyboard.append([InlineKeyboardButton("💳 Купить", callback_data=f"buy_product_{product_id}")])
        
        # Навигация
        keyboard.append([InlineKeyboardButton("◀️ Назад в каталог", callback_data="main_shop")])
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(
            context=context,
            chat_id=chat_id,
            user_id=user_id,
            text=product_details,
            reply_markup=reply_markup,
            parse_mode='Markdown',
            query=query
        )
    
    async def handle_product_purchase(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, product_id: str, user_id: int):
        """Обработка покупки продукта - переход к оплате"""
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
💳 **Оформление заказа**

📦 Продукт: {selected_product['name']}
💰 Цена: {selected_product['price']} руб.

Для завершения покупки свяжитесь с администратором:
📧 Email: admin@example.com
📱 Telegram: @admin_username

Или используйте команду /admin для связи.
            """
            
            keyboard = [
                [InlineKeyboardButton("🌐 Веб-сайт", url="https://telegram-bot-kate.vercel.app")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id, 
                text=payment_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
    
    async def shop_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        """Показать каталог продуктов"""
        chat_id = update.effective_chat.id
        user_id = update.effective_user.id
        
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
        
        await self.send_or_edit_message(
            context=context,
            chat_id=chat_id,
            user_id=user_id,
            text=catalog_text,
            reply_markup=reply_markup,
            parse_mode='Markdown',
            query=query
        )
    
    async def cart_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать корзину"""
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        cart_items = self.db.get_cart(user_id)
        
        if not cart_items:
            cart_text = """
🛒 **Ваша корзина пуста**

Добавьте товары из каталога, чтобы оформить заказ.
            """
            keyboard = [
                [InlineKeyboardButton("💎 В каталог", callback_data="main_shop")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]
        else:
            total = sum(item['price'] * item['quantity'] for item in cart_items)
            cart_text = "🛒 **Ваша корзина:**\n\n"
            
            for item in cart_items:
                cart_text += f"""
📦 **{item['name']}**
💰 {item['price']} руб. × {item['quantity']} = {item['price'] * item['quantity']} руб.
"""
            
            cart_text += f"\n💵 **Итого:** {total} руб."
            
            keyboard = [
                [InlineKeyboardButton("💳 Оформить заказ", callback_data="create_order_from_cart")],
                [InlineKeyboardButton("🗑️ Очистить корзину", callback_data="clear_cart")],
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
    
    async def show_orders_menu(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_id: int, query=None):
        """Показать меню заказов"""
        orders = self.db.get_user_orders(user_id)
        cart_items = self.db.get_cart(user_id)
        
        if not orders and not cart_items:
            orders_text = """
📋 **Мои заказы**

У вас пока нет заказов.

Добавьте товары в корзину и оформите заказ!
            """
            keyboard = [
                [InlineKeyboardButton("💎 В каталог", callback_data="main_shop")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]
        else:
            orders_text = "📋 **Мои заказы**\n\n"
            
            # Показываем прошлые заказы
            if orders:
                orders_text += "📦 **Прошлые заказы:**\n\n"
                for order in orders[:10]:  # Показываем последние 10 заказов
                    status_emoji = "✅" if order['status'] == 'paid' else "⏳" if order['status'] == 'pending' else "❌"
                    orders_text += f"{status_emoji} Заказ #{order['id']} - {order['total_amount']} руб. ({order['status']})\n"
                    orders_text += f"   📅 {order['order_date']}\n\n"
            
            # Если есть товары в корзине, предлагаем оформить заказ
            if cart_items:
                total = sum(item['price'] * item['quantity'] for item in cart_items)
                orders_text += f"\n🛒 **В корзине:** {len(cart_items)} товар(ов) на сумму {total} руб.\n"
            
            keyboard = []
            
            # Кнопки для заказов
            if orders:
                for order in orders[:5]:  # Показываем кнопки для первых 5 заказов
                    keyboard.append([InlineKeyboardButton(
                        f"📦 Заказ #{order['id']} - {order['total_amount']} руб.",
                        callback_data=f"order_details_{order['id']}"
                    )])
            
            # Кнопка оформления заказа из корзины
            if cart_items:
                keyboard.append([InlineKeyboardButton("💳 Оформить заказ из корзины", callback_data="create_order_from_cart")])
            
            keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(
            context=context,
            chat_id=chat_id,
            user_id=user_id,
            text=orders_text,
            reply_markup=reply_markup,
            parse_mode='Markdown',
            query=query
        )
    
    async def show_order_details(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_id: int, order_id: int, query=None):
        """Показать детали заказа"""
        order = self.db.get_order(order_id)
        
        if not order or order['user_id'] != user_id:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Заказ не найден."
            )
            return
        
        # Парсим данные заказа
        order_items = []
        if order.get('data'):
            try:
                if isinstance(order['data'], str):
                    order_items = json.loads(order['data'])
                else:
                    order_items = order['data']
            except:
                order_items = []
        
        status_text = {
            'pending': '⏳ Ожидает оплаты',
            'paid': '✅ Оплачен',
            'cancelled': '❌ Отменен'
        }.get(order['status'], order['status'])
        
        order_details = f"""
📦 **Заказ #{order_id}**

📅 Дата: {order['order_date']}
💰 Сумма: {order['total_amount']} руб.
📊 Статус: {status_text}

📋 **Состав заказа:**
"""
        
        if order_items:
            for item in order_items:
                if isinstance(item, dict):
                    product_name = item.get('name', 'Неизвестный товар')
                    quantity = item.get('quantity', 1)
                    price = item.get('price', 0)
                    order_details += f"• {product_name} × {quantity} = {price * quantity} руб.\n"
        else:
            order_details += "• Детали недоступны\n"
        
        keyboard = []
        
        # Если заказ не оплачен, показываем кнопку оплаты
        if order['status'] == 'pending':
            keyboard.append([InlineKeyboardButton("💳 Оплатить заказ", callback_data=f"pay_order_{order_id}")])
        
        keyboard.append([InlineKeyboardButton("◀️ Назад к заказам", callback_data="main_orders")])
        keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await self.send_or_edit_message(
            context=context,
            chat_id=chat_id,
            user_id=user_id,
            text=order_details,
            reply_markup=reply_markup,
            parse_mode='Markdown',
            query=query
        )
    
    async def create_order_from_cart(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_id: int, query=None):
        """Создание заказа из корзины"""
        cart_items = self.db.get_cart(user_id)
        
        if not cart_items:
            await query.answer("❌ Корзина пуста", show_alert=True) if query else None
            return
        
        # Вычисляем общую сумму
        total = sum(item['price'] * item['quantity'] for item in cart_items)
        
        # Формируем данные заказа
        order_items = []
        for item in cart_items:
            order_items.append({
                'product_id': item['product_id'],
                'name': item['name'],
                'price': item['price'],
                'quantity': item['quantity']
            })
        
        # Создаем заказ
        order_data = {
            'user_id': user_id,
            'total_amount': total,
            'status': 'pending',
            'items': order_items
        }
        
        order_id = self.db.add_order(order_data)
        
        if order_id:
            # Очищаем корзину
            self.db.clear_cart(user_id)
            
            success_text = f"""
✅ **Заказ #{order_id} создан!**

💰 Сумма заказа: {total} руб.

📋 Состав заказа:
"""
            for item in order_items:
                success_text += f"• {item['name']} × {item['quantity']} = {item['price'] * item['quantity']} руб.\n"
            
            success_text += "\n💳 Вы можете оплатить заказ сейчас или позже."
            
            keyboard = [
                [InlineKeyboardButton("💳 Оплатить заказ", callback_data=f"pay_order_{order_id}")],
                [InlineKeyboardButton("📋 Мои заказы", callback_data="main_orders")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await self.send_or_edit_message(
                context=context,
                chat_id=chat_id,
                user_id=user_id,
                text=success_text,
                reply_markup=reply_markup,
                parse_mode='Markdown',
                query=query
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Ошибка при создании заказа. Попробуйте позже."
            )
    
    async def pay_order(self, chat_id: int, context: ContextTypes.DEFAULT_TYPE, user_id: int, order_id: int):
        """Оплата заказа"""
        order = self.db.get_order(order_id)
        
        if not order or order['user_id'] != user_id:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Заказ не найден."
            )
            return
        
        if order['status'] == 'paid':
            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ Этот заказ уже оплачен."
            )
            return
        
        # Если есть обработчик платежей - используем его
        if self.payment_handler:
            # Для оплаты заказа нужно отправить инвойс
            # Пока просто обновляем статус (в реальности здесь будет вызов платежной системы)
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"💳 Оплата заказа #{order_id} на сумму {order['total_amount']} руб.\n\nПлатежная система будет подключена позже."
            )
        else:
            # Если платежей нет - показываем информацию для связи с админом
            payment_text = f"""
💳 **Оплата заказа #{order_id}**

💰 Сумма к оплате: {order['total_amount']} руб.

Для оплаты свяжитесь с администратором:
📧 Email: admin@example.com
📱 Telegram: @admin_username

Или используйте команду /admin для связи.
            """
            
            keyboard = [
                [InlineKeyboardButton("📋 Мои заказы", callback_data="main_orders")],
                [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=payment_text,
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