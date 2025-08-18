import asyncio
import logging
import json
import sqlite3
from datetime import datetime
from typing import List, Dict
from database import Database

logger = logging.getLogger(__name__)

class NotificationSystem:
    """Система уведомлений для бота"""
    
    def __init__(self, database: Database, bot):
        self.db = database
        self.bot = bot
        self.is_running = False
    
    async def start_scheduler(self):
        """Запуск планировщика уведомлений"""
        self.is_running = True
        logger.info("Планировщик уведомлений запущен")
        
        while self.is_running:
            try:
                await self.check_and_send_notifications()
                await asyncio.sleep(60)  # Проверяем каждую минуту
            except Exception as e:
                logger.error(f"Ошибка в планировщике уведомлений: {e}")
                await asyncio.sleep(300)
    
    async def check_and_send_notifications(self):
        """Проверка и отправка запланированных уведомлений"""
        try:
            notifications = self.db.get_pending_notifications()
            
            for notification in notifications:
                if await self.should_send_notification(notification):
                    await self.send_notification(notification)
                    self.db.mark_notification_sent(notification['id'])
        
        except Exception as e:
            logger.error(f"Ошибка при проверке уведомлений: {e}")
    
    async def should_send_notification(self, notification: Dict) -> bool:
        """Проверка, нужно ли отправить уведомление"""
        if notification['is_sent']:
            return False
        
        scheduled_date = notification.get('scheduled_date')
        if not scheduled_date:
            return True
        
        try:
            scheduled = datetime.fromisoformat(scheduled_date)
            return datetime.now() >= scheduled
        except:
            return True
    
    async def send_notification(self, notification: Dict):
        """Отправка уведомления пользователям"""
        try:
            title = notification['title']
            message = notification['message']
            target_audience = notification['target_audience']
            
            full_message = f"""
📢 {title}

{message}

---
Отправлено: {datetime.now().strftime('%d.%m.%Y %H:%M')}
            """
            
            users = self.get_target_users(target_audience)
            sent_count = 0
            
            for user in users:
                try:
                    await self.bot.send_message(
                        chat_id=user['user_id'],
                        text=full_message
                    )
                    sent_count += 1
                    await asyncio.sleep(0.1)
                except Exception as e:
                    logger.error(f"Ошибка отправки уведомления пользователю {user['user_id']}: {e}")
            
            logger.info(f"Уведомление '{title}' отправлено {sent_count} пользователям")
            
        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления: {e}")
    
    def get_target_users(self, target_audience: str) -> List[Dict]:
        """Получение списка целевых пользователей"""
        try:
            if target_audience == 'all':
                return self.db.get_all_users()
            elif target_audience == 'active':
                return self.db.get_active_users()
            elif target_audience == 'new':
                return self.db.get_users_by_date_range(days=7)
            elif target_audience == 'completed':
                return self.db.get_users_by_stage('completed')
            else:
                return []
        except Exception as e:
            logger.error(f"Ошибка при получении целевых пользователей: {e}")
            return []
    
    def stop_scheduler(self):
        """Остановка планировщика"""
        self.is_running = False
        logger.info("Планировщик уведомлений остановлен")

# Дополнительные методы для базы данных
def add_notification_methods_to_db(db_class):
    """Добавляет методы для работы с уведомлениями в класс Database"""
    
    def get_pending_notifications(self):
        """Получение всех неотправленных уведомлений"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM notifications 
                    WHERE is_sent = 0 
                    ORDER BY scheduled_date ASC
                ''')
                rows = cursor.fetchall()
                
                columns = [description[0] for description in cursor.description]
                notifications = []
                
                for row in rows:
                    notification_data = dict(zip(columns, row))
                    notifications.append(notification_data)
                
                return notifications
        except Exception as e:
            print(f"Ошибка при получении уведомлений: {e}")
            return []
    
    def mark_notification_sent(self, notification_id: int) -> bool:
        """Отметка уведомления как отправленного"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE notifications 
                    SET is_sent = 1, sent_date = CURRENT_TIMESTAMP
                    WHERE id = ?
                ''', (notification_id,))
                conn.commit()
                return True
        except Exception as e:
            print(f"Ошибка при отметке уведомления: {e}")
            return False
    
    def get_active_users(self):
        """Получение активных пользователей"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM users 
                    WHERE last_activity >= datetime('now', '-30 days')
                    ORDER BY last_activity DESC
                ''')
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
            print(f"Ошибка при получении активных пользователей: {e}")
            return []
    
    def get_users_by_date_range(self, days: int):
        """Получение пользователей по диапазону дат"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM users 
                    WHERE registration_date >= datetime('now', '-{} days')
                    ORDER BY registration_date DESC
                '''.format(days))
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
            print(f"Ошибка при получении пользователей по датам: {e}")
            return []
    
    def get_users_by_stage(self, stage: str):
        """Получение пользователей по этапу"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT * FROM users 
                    WHERE stage = ?
                    ORDER BY registration_date DESC
                ''', (stage,))
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
            print(f"Ошибка при получении пользователей по этапу: {e}")
            return []
    
    # Добавляем методы в класс Database
    db_class.get_pending_notifications = get_pending_notifications
    db_class.mark_notification_sent = mark_notification_sent
    db_class.get_active_users = get_active_users
    db_class.get_users_by_date_range = get_users_by_date_range
    db_class.get_users_by_stage = get_users_by_stage 