import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

from database import Database
from config import *
from handlers import UserHandlers, AdminHandlers
from notifications import NotificationSystem, add_notification_methods_to_db

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        # Инициализация базы данных
        self.db = Database(DATABASE_PATH)
        add_notification_methods_to_db(self.db)
        
        # Создание приложения
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Инициализация обработчиков
        self.user_handlers = UserHandlers(self.db)
        self.admin_handlers = AdminHandlers(self.db)
        self.notification_system = NotificationSystem(self.db, self.application.bot)
        
        # Настройка обработчиков
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка всех обработчиков команд и сообщений"""
        # Основные команды
        self.application.add_handler(CommandHandler("start", self.user_handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.user_handlers.help_command))
        
        # Админ команды
        self.application.add_handler(CommandHandler("admin", self.admin_handlers.admin_command))
        self.application.add_handler(CommandHandler("meeting", self.admin_handlers.meeting_command))
        self.application.add_handler(CommandHandler("offer", self.admin_handlers.offer_command))
        
        # Обработчики сообщений и callback
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.user_handlers.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.user_handlers.handle_callback))
    
    def run(self):
        """Запуск бота"""
        logger.info("🚀 Запуск Telegram бота...")
        self.application.run_polling()

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run() 