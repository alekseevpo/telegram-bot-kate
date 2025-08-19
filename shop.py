from typing import Dict, List, Optional
from datetime import datetime
import json
from database import Database

class Shop:
    """Модуль магазина для Telegram бота"""
    
    def __init__(self, database: Database):
        self.db = database
        self.carts = {}  # user_id -> cart_items
    
    def get_products(self) -> List[Dict]:
        """Получение всех доступных продуктов"""
        products = self.db.get_products()
        
        if not products:
            # Создаем базовые продукты, если их нет
            self.db.add_product("Базовый курс", 5000, "Полный курс по основам метода работы")
            self.db.add_product("Продвинутый курс", 10000, "Углубленное изучение продвинутых техник")
            self.db.add_product("Индивидуальная консультация", 3000, "Персональная консультация 1-на-1")
            self.db.add_product("Групповой мастер-класс", 1500, "Участие в групповом мастер-классе")
            products = self.db.get_products()
        
        return products
    
    def add_to_cart(self, user_id: int, product_id: int, quantity: int = 1) -> bool:
        """Добавление товара в корзину"""
        try:
            if user_id not in self.carts:
                self.carts[user_id] = []
            
            # Проверяем, есть ли уже такой товар в корзине
            for item in self.carts[user_id]:
                if item['product_id'] == product_id:
                    item['quantity'] += quantity
                    return True
            
            # Получаем информацию о продукте
            products = self.db.get_products()
            product = None
            for p in products:
                if p['id'] == product_id:
                    product = p
                    break
            
            if not product:
                return False
            
            # Добавляем в корзину
            cart_item = {
                'product_id': product_id,
                'name': product['name'],
                'price': product['price'],
                'quantity': quantity,
                'total': product['price'] * quantity
            }
            
            self.carts[user_id].append(cart_item)
            return True
            
        except Exception as e:
            print(f"Ошибка при добавлении в корзину: {e}")
            return False
    
    def remove_from_cart(self, user_id: int, product_id: int) -> bool:
        """Удаление товара из корзины"""
        try:
            if user_id not in self.carts:
                return False
            
            self.carts[user_id] = [item for item in self.carts[user_id] if item['product_id'] != product_id]
            return True
            
        except Exception as e:
            print(f"Ошибка при удалении из корзины: {e}")
            return False
    
    def get_cart(self, user_id: int) -> List[Dict]:
        """Получение содержимого корзины"""
        return self.carts.get(user_id, [])
    
    def get_cart_total(self, user_id: int) -> int:
        """Получение общей суммы корзины"""
        cart = self.get_cart(user_id)
        return sum(item['total'] for item in cart)
    
    def clear_cart(self, user_id: int) -> bool:
        """Очистка корзины"""
        try:
            if user_id in self.carts:
                del self.carts[user_id]
            return True
        except Exception as e:
            print(f"Ошибка при очистке корзины: {e}")
            return False
    
    def create_order(self, user_id: int, user_data: Dict) -> Optional[Dict]:
        """Создание заказа"""
        try:
            cart = self.get_cart(user_id)
            if not cart:
                return None
            
            total_amount = self.get_cart_total(user_id)
            
            # Создаем заказ в базе данных
            order_data = {
                'user_id': user_id,
                'total_amount': total_amount,
                'status': 'pending',
                'items': cart,
                'user_info': user_data,
                'created_at': datetime.now().isoformat()
            }
            
            # Сохраняем заказ в базе
            order_id = self.db.add_order(order_data)
            
            if order_id:
                # Очищаем корзину
                self.clear_cart(user_id)
                
                return {
                    'order_id': order_id,
                    'total_amount': total_amount,
                    'items': cart,
                    'status': 'pending'
                }
            
            return None
            
        except Exception as e:
            print(f"Ошибка при создании заказа: {e}")
            return None
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """Получение информации о заказе"""
        return self.db.get_order(order_id)
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Обновление статуса заказа"""
        return self.db.update_order_status(order_id, status)
    
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Получение всех заказов пользователя"""
        return self.db.get_user_orders(user_id)
    
    def format_cart_message(self, user_id: int) -> str:
        """Форматирование сообщения корзины"""
        cart = self.get_cart(user_id)
        
        if not cart:
            return "🛒 Ваша корзина пуста"
        
        message = "🛒 Ваша корзина:\n\n"
        
        for item in cart:
            message += f"├── {item['name']} x{item['quantity']} - {item['total']}₽\n"
        
        total = self.get_cart_total(user_id)
        message += f"└── **Итого: {total}₽**\n\n"
        
        return message
    
    def format_products_catalog(self) -> str:
        """Форматирование каталога продуктов"""
        products = self.get_products()
        
        message = "💎 **Каталог продуктов:**\n\n"
        
        for product in products:
            message += f"""
**{product['name']}** - {product['price']}₽
📝 {product['description']}
🆔 ID: `{product['id']}`

"""
        
        message += "💡 **Как купить:**\n"
        message += "1. Выберите продукт по ID\n"
        message += "2. Добавьте в корзину: `/add ID`\n"
        message += "3. Оформите заказ: `/cart`\n\n"
        
        message += "🌐 **Веб-версия:**\n"
        message += "📱 Откройте наш сайт для удобного просмотра:\n"
        message += "🔗 https://telegram-bot-kate-qbdv.vercel.app\n\n"
        
        message += "💻 **Преимущества веб-версии:**\n"
        message += "• Красивый каталог с фото\n"
        message += "• Удобная навигация\n"
        message += "• Мобильная версия\n"
        message += "• Быстрый доступ к услугам"
        
        return message


class PaymentProcessor:
    """Обработчик платежей (заглушка для интеграции с ЮKassa)"""
    
    def __init__(self):
        self.api_key = None
        self.secret_key = None
        self.shop_id = None
    
    def setup_yookassa(self, api_key: str, secret_key: str, shop_id: str):
        """Настройка ЮKassa"""
        self.api_key = api_key
        self.secret_key = secret_key
        self.shop_id = shop_id
    
    def create_payment(self, order_id: str, amount: int, description: str) -> Dict:
        """Создание платежа (заглушка)"""
        # Здесь будет реальная интеграция с ЮKassa
        return {
            'payment_id': f'payment_{order_id}',
            'amount': amount,
            'status': 'pending',
            'payment_url': f'https://yoomoney.ru/checkout/payments/v2/contract?orderId={order_id}',
            'confirmation_url': f'https://yoomoney.ru/checkout/payments/v2/contract?orderId={order_id}'
        }
    
    def check_payment_status(self, payment_id: str) -> str:
        """Проверка статуса платежа (заглушка)"""
        # Здесь будет реальная проверка через API ЮKassa
        return 'pending'
    
    def process_payment_webhook(self, webhook_data: Dict) -> bool:
        """Обработка webhook от ЮKassa (заглушка)"""
        # Здесь будет реальная обработка webhook
        return True 