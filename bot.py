import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, PreCheckoutQueryHandler, filters, ContextTypes

from database import Database
from config import *
from handlers import UserHandlers, AdminHandlers
from notifications import NotificationSystem, add_notification_methods_to_db
from payments import PaymentHandler

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
        self.payment_handler = PaymentHandler(PAYMENT_PROVIDER_TOKEN, self.db) if PAYMENT_PROVIDER_TOKEN else None
        
        # Передаём payment_handler в user_handlers
        self.user_handlers.payment_handler = self.payment_handler
        
        # Настройка обработчиков
        self.setup_handlers()
    
    def setup_handlers(self):
        """Настройка всех обработчиков команд и сообщений"""
        # Основные команды
        self.application.add_handler(CommandHandler("start", self.user_handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.user_handlers.help_command))
        
        # Команды магазина
        self.application.add_handler(CommandHandler("shop", self.user_handlers.shop_command))
        self.application.add_handler(CommandHandler("cart", self.user_handlers.cart_command))
        self.application.add_handler(CommandHandler("add", self.user_handlers.add_to_cart_command))
        
        # Админ команды
        self.application.add_handler(CommandHandler("admin", self.admin_handlers.admin_command))
        self.application.add_handler(CommandHandler("meeting", self.admin_handlers.meeting_command))
        self.application.add_handler(CommandHandler("offer", self.admin_handlers.offer_command))
        
        # Обработчики платежей (только если токен настроен)
        if self.payment_handler:
            self.application.add_handler(PreCheckoutQueryHandler(self.payment_handler.pre_checkout_query))
            self.application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, self.payment_handler.successful_payment))
            logger.info("✅ Обработчики платежей подключены")
        else:
            logger.warning("⚠️ Обработчики платежей отключены (токен не настроен)")
        
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