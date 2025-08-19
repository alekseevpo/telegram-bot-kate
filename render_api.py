from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import List, Optional, Dict
from datetime import datetime
import json
import os
from database import Database
from config import ADMIN_ID, DATABASE_PATH

# Инициализация FastAPI
app = FastAPI(
    title="Kate Bot Admin API",
    description="API для веб-интерфейса администратора Telegram бота",
    version="1.0.0"
)

# CORS middleware для работы с Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://*.vercel.app",  # Vercel домены
        "https://*.vercel.app/*",  # Vercel поддомены
        "http://localhost:3000",   # Локальная разработка
        "http://localhost:8000"    # Локальный API
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Инициализация базы данных
db = Database(DATABASE_PATH)

# Модели данных
class ProductCreate(BaseModel):
    name: str
    price: int
    description: str

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    description: Optional[str] = None

class UserUpdate(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    stage: Optional[str] = None
    phone: Optional[str] = None

class NotificationCreate(BaseModel):
    message: str
    target_audience: Optional[str] = "all"
    send_time: Optional[str] = None

# Простая аутентификация
security = HTTPBearer()

def verify_admin(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Проверка прав администратора"""
    token = credentials.credentials
    # В реальном приложении здесь должна быть более серьезная проверка
    if token != f"admin_{ADMIN_ID}":
        raise HTTPException(status_code=403, detail="Доступ запрещен")
    return True

# === ЭНДПОИНТЫ ===

@app.get("/")
async def root():
    """Корневой эндпоинт"""
    return {"message": "Kate Bot Admin API", "version": "1.0.0"}

@app.get("/health")
async def health():
    """Проверка здоровья API"""
    return {"status": "ok", "timestamp": datetime.now().isoformat()}

# === АНАЛИТИКА И ДАШБОРД ===

@app.get("/api/dashboard/stats")
async def get_dashboard_stats(admin: bool = Depends(verify_admin)):
    """Получение основной статистики для дашборда"""
    try:
        users = db.get_all_users()
        orders = db.execute_query("SELECT * FROM orders")
        products = db.get_products()
        
        # Подсчет статистики
        total_users = len(users)
        total_orders = len(orders)
        total_products = len(products)
        
        # Доходы
        total_revenue = sum(order.get('total_amount', 0) for order in orders if order.get('status') == 'completed')
        
        # Новые пользователи за сегодня
        today = datetime.now().strftime('%Y-%m-%d')
        new_users_today = len([u for u in users if u.get('registration_date', '').startswith(today)])
        
        # Популярные продукты
        product_sales = {}
        for order in orders:
            if order.get('data'):
                try:
                    order_data = json.loads(order['data'])
                    items = order_data.get('items', [])
                    for item in items:
                        product_id = item.get('product_id')
                        if product_id:
                            product_sales[product_id] = product_sales.get(product_id, 0) + item.get('quantity', 1)
                except:
                    pass
        
        return {
            "total_users": total_users,
            "total_orders": total_orders,
            "total_products": total_products,
            "total_revenue": total_revenue,
            "new_users_today": new_users_today,
            "product_sales": product_sales
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения статистики: {str(e)}")

# === УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ ===

@app.get("/api/users")
async def get_users(admin: bool = Depends(verify_admin)):
    """Получение списка всех пользователей"""
    try:
        users = db.get_all_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения пользователей: {str(e)}")

@app.get("/api/users/{user_id}")
async def get_user(user_id: int, admin: bool = Depends(verify_admin)):
    """Получение информации о пользователе"""
    try:
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Получаем заказы пользователя
        orders = db.get_user_orders(user_id)
        
        return {"user": user, "orders": orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения пользователя: {str(e)}")

@app.put("/api/users/{user_id}")
async def update_user(user_id: int, user_data: UserUpdate, admin: bool = Depends(verify_admin)):
    """Обновление информации о пользователе"""
    try:
        user = db.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        # Обновляем поля
        update_fields = {}
        if user_data.name is not None:
            update_fields['name'] = user_data.name
        if user_data.gender is not None:
            update_fields['gender'] = user_data.gender
        if user_data.stage is not None:
            update_fields['stage'] = user_data.stage
        if user_data.phone is not None:
            update_fields['phone'] = user_data.phone
        
        if update_fields:
            db.update_user(user_id, **update_fields)
        
        return {"message": "Пользователь обновлен", "user_id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления пользователя: {str(e)}")

# === УПРАВЛЕНИЕ ПРОДУКТАМИ ===

@app.get("/api/products")
async def get_products():
    """Получение списка всех продуктов (публичный доступ)"""
    try:
        products = db.get_products()
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения продуктов: {str(e)}")

@app.get("/api/admin/products")
async def get_admin_products(admin: bool = Depends(verify_admin)):
    """Получение списка всех продуктов (только для админа)"""
    try:
        products = db.get_products()
        return {"products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения продуктов: {str(e)}")

@app.post("/api/products")
async def create_product(product: ProductCreate, admin: bool = Depends(verify_admin)):
    """Создание нового продукта"""
    try:
        product_id = db.add_product(product.name, product.price, product.description)
        return {"message": "Продукт создан", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания продукта: {str(e)}")

@app.put("/api/products/{product_id}")
async def update_product(product_id: int, product: ProductUpdate, admin: bool = Depends(verify_admin)):
    """Обновление продукта"""
    try:
        # Проверяем, существует ли продукт
        products = db.get_products()
        existing_product = next((p for p in products if p['id'] == product_id), None)
        if not existing_product:
            raise HTTPException(status_code=404, detail="Продукт не найден")
        
        # Обновляем продукт
        query = "UPDATE products SET "
        params = []
        updates = []
        
        if product.name is not None:
            updates.append("name = ?")
            params.append(product.name)
        if product.price is not None:
            updates.append("price = ?")
            params.append(product.price)
        if product.description is not None:
            updates.append("description = ?")
            params.append(product.description)
        
        if updates:
            query += ", ".join(updates) + " WHERE product_id = ?"
            params.append(product_id)
            db.execute_query(query, params)
        
        return {"message": "Продукт обновлен", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления продукта: {str(e)}")

@app.delete("/api/products/{product_id}")
async def delete_product(product_id: int, admin: bool = Depends(verify_admin)):
    """Удаление продукта"""
    try:
        db.execute_query("DELETE FROM products WHERE product_id = ?", (product_id,))
        return {"message": "Продукт удален", "product_id": product_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления продукта: {str(e)}")

# === УПРАВЛЕНИЕ ЗАКАЗАМИ ===

@app.get("/api/orders")
async def get_orders(admin: bool = Depends(verify_admin)):
    """Получение списка всех заказов"""
    try:
        orders = db.execute_query("SELECT * FROM orders ORDER BY order_date DESC")
        
        # Обогащаем заказы информацией о пользователях
        enriched_orders = []
        for order in orders:
            user = db.get_user(order['user_id'])
            order_with_user = dict(order)
            order_with_user['user'] = user
            
            # Парсим данные заказа
            if order.get('data'):
                try:
                    order_with_user['items'] = json.loads(order['data'])
                except:
                    order_with_user['items'] = {}
            
            enriched_orders.append(order_with_user)
        
        return {"orders": enriched_orders}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения заказов: {str(e)}")

@app.put("/api/orders/{order_id}/status")
async def update_order_status(order_id: int, status: str, admin: bool = Depends(verify_admin)):
    """Обновление статуса заказа"""
    try:
        valid_statuses = ['pending', 'confirmed', 'completed', 'cancelled']
        if status not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"Неверный статус. Доступные: {valid_statuses}")
        
        db.update_order_status(order_id, status)
        return {"message": "Статус заказа обновлен", "order_id": order_id, "status": status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка обновления статуса заказа: {str(e)}")

# === УВЕДОМЛЕНИЯ ===

@app.post("/api/notifications")
async def create_notification(notification: NotificationCreate, admin: bool = Depends(verify_admin)):
    """Создание уведомления"""
    try:
        # Планируем отправку уведомления
        send_time = notification.send_time or datetime.now().isoformat()
        
        notification_id = db.add_notification(
            message=notification.message,
            target_audience=notification.target_audience,
            send_time=send_time
        )
        
        return {"message": "Уведомление создано", "notification_id": notification_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка создания уведомления: {str(e)}")

@app.get("/api/notifications")
async def get_notifications(admin: bool = Depends(verify_admin)):
    """Получение списка уведомлений"""
    try:
        notifications = db.execute_query("SELECT * FROM notifications ORDER BY created_at DESC")
        return {"notifications": notifications}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка получения уведомлений: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port) 