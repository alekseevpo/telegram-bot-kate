import axios from 'axios'

// Создаем экземпляр axios с базовой конфигурацией
const api = axios.create({
  baseURL: '/api',
  timeout: 10000
})

// Интерцептор для добавления токена авторизации
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Интерцептор для обработки ошибок
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 403) {
      localStorage.removeItem('admin_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// API методы
export const apiService = {
  // Авторизация
  login(adminId) {
    const token = `admin_${adminId}`
    localStorage.setItem('admin_token', token)
    return Promise.resolve({ token })
  },

  // Публичные методы (без авторизации)
  async getPublicProducts() {
    const response = await fetch('/api/products')
    if (response.ok) {
      const data = await response.json()
      return data.products || []
    }
    throw new Error('Ошибка загрузки продуктов')
  },

  // Дашборд
  async getDashboardStats() {
    const response = await api.get('/dashboard/stats')
    return response.data
  },

  // Пользователи
  async getUsers() {
    const response = await api.get('/users')
    return response.data.users
  },

  async getUser(userId) {
    const response = await api.get(`/users/${userId}`)
    return response.data
  },

  async updateUser(userId, userData) {
    const response = await api.put(`/users/${userId}`, userData)
    return response.data
  },

  // Продукты
  async getProducts() {
    const response = await api.get('/admin/products')
    return response.data.products
  },

  async createProduct(productData) {
    const response = await api.post('/products', productData)
    return response.data
  },

  async updateProduct(productId, productData) {
    const response = await api.put(`/products/${productId}`, productData)
    return response.data
  },

  async deleteProduct(productId) {
    const response = await api.delete(`/products/${productId}`)
    return response.data
  },

  // Заказы
  async getOrders() {
    const response = await api.get('/orders')
    return response.data.orders
  },

  async updateOrderStatus(orderId, status) {
    const response = await api.put(`/orders/${orderId}/status`, null, {
      params: { status }
    })
    return response.data
  },

  // Уведомления
  async getNotifications() {
    const response = await api.get('/notifications')
    return response.data.notifications
  },

  async createNotification(notificationData) {
    const response = await api.post('/notifications', notificationData)
    return response.data
  }
}

export default api 