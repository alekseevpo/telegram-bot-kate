"""
Модуль для работы с платежами через ЮКассу
"""

import logging
from telegram import Update, LabeledPrice, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)

class PaymentHandler:
    """Обработчик платежей через ЮКассу"""
    
    def __init__(self, payment_token: str, database):
        """
        Инициализация обработчика платежей
        
        Args:
            payment_token: Токен провайдера платежей от @BotFather
            database: Экземпляр базы данных
        """
        self.payment_token = payment_token
        self.db = database
    
    async def send_invoice(
        self, 
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE,
        product_id: int
    ):
        """
        Отправка инвойса для оплаты продукта
        
        Args:
            update: Update объект
            context: Context объект
            product_id: ID продукта для покупки
        """
        chat_id = update.effective_chat.id
        
        # Получаем информацию о продукте
        products = self.db.get_products()
        product = None
        
        for p in products:
            if p['id'] == product_id:
                product = p
                break
        
        if not product:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Продукт не найден."
            )
            return
        
        # Формируем название и описание
        title = product['name']
        description = product['description']
        
        # Payload - данные, которые вернутся при успешной оплате
        payload = f"product_{product_id}"
        
        # Цена в копейках (ЮКасса работает в копейках)
        # Важно: amount должен быть целым числом (int)
        prices = [LabeledPrice(label=product['name'], amount=int(product['price'] * 100))]
        
        # Отправляем инвойс
        try:
            await context.bot.send_invoice(
                chat_id=chat_id,
                title=title,
                description=description,
                payload=payload,
                provider_token=self.payment_token,
                currency='RUB',
                prices=prices,
                start_parameter='payment',
                photo_url='https://telegram-bot-kate-qbdv.vercel.app/og-image.jpg',
                photo_width=800,
                photo_height=600,
                need_name=True,
                need_phone_number=True,
                need_email=True,
                is_flexible=False
            )
            
            logger.info(f"Инвойс отправлен пользователю {chat_id} для продукта {product_id}")
            
        except Exception as e:
            logger.error(f"Ошибка при отправке инвойса: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"❌ Ошибка при создании платежа: {str(e)}"
            )
    
    async def handle_precheckout_query(
        self, 
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Обработка pre-checkout запроса (подтверждение перед оплатой)
        """
        query = update.pre_checkout_query
        
        # Проверяем данные заказа
        # В реальном приложении здесь можно проверить наличие товара, скидки и т.д.
        
        try:
            # Подтверждаем платеж
            await query.answer(ok=True)
            logger.info(f"Pre-checkout подтвержден для {query.from_user.id}")
            
        except Exception as e:
            # Отклоняем платеж с сообщением об ошибке
            await query.answer(
                ok=False, 
                error_message=f"Ошибка при обработке платежа: {str(e)}"
            )
            logger.error(f"Ошибка в pre-checkout: {e}")
    
    async def handle_successful_payment(
        self, 
        update: Update, 
        context: ContextTypes.DEFAULT_TYPE
    ):
        """
        Обработка успешного платежа
        """
        payment = update.message.successful_payment
        user_id = update.effective_user.id
        chat_id = update.effective_chat.id
        
        # Извлекаем ID продукта из payload
        payload = payment.invoice_payload
        product_id = int(payload.split('_')[1])
        
        # Получаем информацию о продукте
        products = self.db.get_products()
        product = None
        
        for p in products:
            if p['id'] == product_id:
                product = p
                break
        
        if not product:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Ошибка: продукт не найден."
            )
            return
        
        # Сохраняем заказ в базу данных
        try:
            order_id = self.db.create_order(
                user_id=user_id,
                product_id=product_id,
                amount=int(payment.total_amount // 100),  # Конвертируем из копеек в рубли
                payment_id=payment.telegram_payment_charge_id
            )
            
            # Отправляем подтверждение
            confirmation_text = f"""
✅ **Оплата успешно получена!**

🎉 Спасибо за покупку!

📦 **Детали заказа:**
🆔 Номер заказа: #{order_id}
💎 Продукт: {product['name']}
💰 Сумма: {int(payment.total_amount // 100)} руб.

📧 Мы отправили подробную информацию на email: {payment.order_info.email}

📱 Также свяжемся с вами по телефону: {payment.order_info.phone_number}

🎓 Доступ к материалам будет предоставлен в течение 5 минут.

Если у вас есть вопросы, напишите в поддержку или используйте главное меню.
            """
            
            keyboard = [[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await context.bot.send_message(
                chat_id=chat_id,
                text=confirmation_text,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            logger.info(f"Успешный платеж от {user_id}: заказ #{order_id}, продукт {product_id}")
            
        except Exception as e:
            logger.error(f"Ошибка при обработке успешного платежа: {e}")
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ Произошла ошибка при сохранении заказа. Пожалуйста, свяжитесь с поддержкой."
            )

