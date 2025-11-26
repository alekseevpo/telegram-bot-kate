import sqlite3
import json
from datetime import datetime
from typing import Optional, Dict, List

class Database:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Инициализация базы данных и создание таблиц"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Таблица пользователей
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    first_name TEXT,
                    last_name TEXT,
                    gender TEXT,
                    name TEXT,
                    phone TEXT,
                    email TEXT,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    stage TEXT DEFAULT 'start',
                    last_message_id INTEGER,
                    data JSON
                )
            ''')
            
            # Миграция: добавляем поле last_message_id, если его нет
            try:
                cursor.execute('ALTER TABLE users ADD COLUMN last_message_id INTEGER')
            except sqlite3.OperationalError:
                pass  # Поле уже существует
            
            # Таблица платных продуктов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price REAL NOT NULL,
                    description TEXT,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # Таблица заказов
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    total_amount REAL,
                    status TEXT DEFAULT 'pending',
                    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    data TEXT
                )
            ''')
            
            # Таблица уведомлений
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS notifications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    message TEXT NOT NULL,
                    target_audience TEXT DEFAULT 'all',
                    scheduled_date TIMESTAMP,
                    sent_date TIMESTAMP,
                    is_sent BOOLEAN DEFAULT 0
                )
            ''')
            
            conn.commit()
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None) -> bool:
        """Добавление нового пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, username, first_name, last_name))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при добавлении пользователя: {e}")
            return False
    
    def update_user_stage(self, user_id: int, stage: str) -> bool:
        """Обновление этапа пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET stage = ?, last_activity = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (stage, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при обновлении этапа: {e}")
            return False
    
    def update_user_data(self, user_id: int, field: str, value: str) -> bool:
        """Обновление данных пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE users SET {field} = ?, last_activity = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                ''', (value, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при обновлении данных: {e}")
            return False
    
    def get_user(self, user_id: int) -> Optional[Dict]:
        """Получение данных пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
                row = cursor.fetchone()
                
                if row:
                    columns = [description[0] for description in cursor.description]
                    user_data = dict(zip(columns, row))
                    
                    # Парсим JSON данные
                    if user_data.get('data'):
                        try:
                            user_data['data'] = json.loads(user_data['data'])
                        except:
                            user_data['data'] = {}
                    
                    return user_data
                return None
        except Exception as e:
            print(f"Ошибка при получении пользователя: {e}")
            return None
    
    def get_all_users(self) -> List[Dict]:
        """Получение всех пользователей"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM users ORDER BY registration_date DESC')
                rows = cursor.fetchall()
                
                columns = [description[0] for description in cursor.description]
                users = []
                
                for row in rows:
                    user_data = dict(zip(columns, row))
                    if user_data.get('data'):
                        try:
                            user_data['data'] = json.loads(user_data['data'])
                        except:
                            user_data['data'] = {}
                    users.append(user_data)
                
                return users
        except Exception as e:
            print(f"Ошибка при получении пользователей: {e}")
            return []
    
    def add_product(self, name: str, price: float, description: str) -> bool:
        """Добавление продукта"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO products (name, price, description)
                    VALUES (?, ?, ?)
                ''', (name, price, description))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при добавлении продукта: {e}")
            return False
    
    def get_products(self) -> List[Dict]:
        """Получение всех активных продуктов"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM products WHERE is_active = 1')
                rows = cursor.fetchall()
                
                columns = [description[0] for description in cursor.description]
                products = []
                
                for row in rows:
                    product_data = dict(zip(columns, row))
                    products.append(product_data)
                
                return products
        except Exception as e:
            print(f"Ошибка при получении продуктов: {e}")
            return []
    
    def add_notification(self, title: str, message: str, target_audience: str = 'all', scheduled_date: str = None) -> bool:
        """Добавление уведомления"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO notifications (title, message, target_audience, scheduled_date)
                    VALUES (?, ?, ?, ?)
                ''', (title, message, target_audience, scheduled_date))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при добавлении уведомления: {e}")
            return False
    
    def add_order(self, order_data: dict) -> Optional[int]:
        """Добавление заказа"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Добавляем заказ
                cursor.execute('''
                    INSERT INTO orders (user_id, total_amount, status, order_date)
                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ''', (order_data['user_id'], order_data['total_amount'], order_data['status']))
                
                order_id = cursor.lastrowid
                
                # Сохраняем детали заказа в JSON поле
                cursor.execute('''
                    UPDATE orders SET data = ? WHERE id = ?
                ''', (json.dumps(order_data), order_id))
                
                conn.commit()
                return order_id
        except Exception as e:
            print(f"Ошибка при добавлении заказа: {e}")
            return None
    
    def get_order(self, order_id: int) -> Optional[Dict]:
        """Получение заказа по ID"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
                row = cursor.fetchone()
                
                if row:
                    columns = [description[0] for description in cursor.description]
                    order_data = dict(zip(columns, row))
                    
                    # Парсим JSON данные
                    if order_data.get('data'):
                        try:
                            order_data['data'] = json.loads(order_data['data'])
                        except:
                            order_data['data'] = {}
                    
                    return order_data
                return None
        except Exception as e:
            print(f"Ошибка при получении заказа: {e}")
            return None
    
    def update_order_status(self, order_id: int, status: str) -> bool:
        """Обновление статуса заказа"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE orders SET status = ? WHERE id = ?
                ''', (status, order_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при обновлении статуса заказа: {e}")
            return False
    
    def get_user_orders(self, user_id: int) -> List[Dict]:
        """Получение всех заказов пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM orders WHERE user_id = ? ORDER BY order_date DESC
                ''', (user_id,))
                rows = cursor.fetchall()
                
                columns = [description[0] for description in cursor.description]
                orders = []
                
                for row in rows:
                    order_data = dict(zip(columns, row))
                    if order_data.get('data'):
                        try:
                            order_data['data'] = json.loads(order_data['data'])
                        except:
                            order_data['data'] = {}
                    orders.append(order_data)
                
                return orders
        except Exception as e:
            print(f"Ошибка при получении заказов пользователя: {e}")
            return []
    
    def create_order(self, user_id: int, product_id: int, amount: float, payment_id: str = None) -> int:
        """
        Создание нового заказа
        
        Args:
            user_id: ID пользователя
            product_id: ID продукта
            amount: Сумма заказа
            payment_id: ID платежа от платежной системы
        
        Returns:
            ID созданного заказа или 0 при ошибке
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Данные заказа в JSON
                order_data = {
                    'product_id': product_id,
                    'payment_id': payment_id,
                    'order_date': datetime.now().isoformat()
                }
                
                cursor.execute('''
                    INSERT INTO orders (user_id, total_amount, status, data)
                    VALUES (?, ?, 'paid', ?)
                ''', (user_id, amount, json.dumps(order_data)))
                
                conn.commit()
                return cursor.lastrowid
        except Exception as e:
            print(f"Ошибка при создании заказа: {e}")
            return 0
    
    def update_last_message_id(self, user_id: int, message_id: int) -> bool:
        """Обновление ID последнего сообщения бота для пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET last_message_id = ? WHERE user_id = ?
                ''', (message_id, user_id))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при обновлении last_message_id: {e}")
            return False
    
    def get_last_message_id(self, user_id: int) -> Optional[int]:
        """Получение ID последнего сообщения бота для пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT last_message_id FROM users WHERE user_id = ?', (user_id,))
                row = cursor.fetchone()
                return row[0] if row else None
        except Exception as e:
            print(f"Ошибка при получении last_message_id: {e}")
            return None 