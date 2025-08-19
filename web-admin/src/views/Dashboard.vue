<template>
  <div>
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold mb-2">📊 Дашборд</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Обзор статистики и аналитики бота</p>
      </v-col>
    </v-row>

    <!-- Карточки статистики -->
    <v-row class="mb-6">
      <v-col cols="12" sm="6" md="3">
        <v-card color="primary" dark>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" class="mr-4">mdi-account-group</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ stats.total_users || 0 }}</div>
                <div class="text-caption">Всего пользователей</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card color="success" dark>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" class="mr-4">mdi-cart</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ stats.total_orders || 0 }}</div>
                <div class="text-caption">Всего заказов</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card color="warning" dark>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" class="mr-4">mdi-currency-rub</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ formatMoney(stats.total_revenue || 0) }}</div>
                <div class="text-caption">Общий доход</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" sm="6" md="3">
        <v-card color="info" dark>
          <v-card-text>
            <div class="d-flex align-center">
              <v-icon size="40" class="mr-4">mdi-account-plus</v-icon>
              <div>
                <div class="text-h4 font-weight-bold">{{ stats.new_users_today || 0 }}</div>
                <div class="text-caption">Новых за сегодня</div>
              </div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Быстрые действия -->
    <v-row class="mb-6">
      <v-col cols="12">
        <v-card>
          <v-card-title>
            <v-icon class="mr-2">mdi-lightning-bolt</v-icon>
            Быстрые действия
          </v-card-title>
          <v-card-text>
            <v-row>
              <v-col cols="12" sm="6" md="3">
                <v-btn 
                  color="primary" 
                  variant="outlined" 
                  block 
                  @click="$router.push('/users')"
                  prepend-icon="mdi-account-group"
                >
                  Пользователи
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn 
                  color="success" 
                  variant="outlined" 
                  block 
                  @click="$router.push('/products')"
                  prepend-icon="mdi-package-variant"
                >
                  Продукты
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn 
                  color="warning" 
                  variant="outlined" 
                  block 
                  @click="$router.push('/orders')"
                  prepend-icon="mdi-cart"
                >
                  Заказы
                </v-btn>
              </v-col>
              <v-col cols="12" sm="6" md="3">
                <v-btn 
                  color="info" 
                  variant="outlined" 
                  block 
                  @click="$router.push('/notifications')"
                  prepend-icon="mdi-bell"
                >
                  Уведомления
                </v-btn>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <!-- Последние действия -->
    <v-row>
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>
            <v-icon class="mr-2">mdi-history</v-icon>
            Последние заказы
          </v-card-title>
          <v-card-text>
            <v-table v-if="recentOrders.length > 0">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Пользователь</th>
                  <th>Сумма</th>
                  <th>Статус</th>
                  <th>Дата</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="order in recentOrders" :key="order.id">
                  <td>{{ order.id }}</td>
                  <td>{{ order.user?.name || 'Неизвестен' }}</td>
                  <td>{{ formatMoney(order.total_amount || 0) }}</td>
                  <td>
                    <v-chip 
                      :color="getStatusColor(order.status)" 
                      size="small"
                    >
                      {{ getStatusText(order.status) }}
                    </v-chip>
                  </td>
                  <td>{{ formatDate(order.order_date) }}</td>
                </tr>
              </tbody>
            </v-table>
            <div v-else class="text-center py-8 text-medium-emphasis">
              <v-icon size="48" class="mb-4">mdi-cart-off</v-icon>
              <div>Заказов пока нет</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
      
      <v-col cols="12" md="4">
        <v-card>
          <v-card-title>
            <v-icon class="mr-2">mdi-trending-up</v-icon>
            Популярные продукты
          </v-card-title>
          <v-card-text>
            <div v-if="Object.keys(stats.product_sales || {}).length > 0">
              <div v-for="(sales, productId) in stats.product_sales" :key="productId" class="mb-3">
                <div class="d-flex justify-space-between align-center">
                  <span>Продукт #{{ productId }}</span>
                  <v-chip size="small" color="primary">{{ sales }}</v-chip>
                </div>
                <v-progress-linear 
                  :model-value="(sales / Math.max(...Object.values(stats.product_sales))) * 100"
                  color="primary"
                  height="4"
                  class="mt-1"
                ></v-progress-linear>
              </div>
            </div>
            <div v-else class="text-center py-8 text-medium-emphasis">
              <v-icon size="48" class="mb-4">mdi-chart-line</v-icon>
              <div>Данных пока нет</div>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import { apiService } from '../services/api.js'

export default {
  name: 'Dashboard',
  setup() {
    const stats = ref({})
    const recentOrders = ref([])
    const loading = ref(false)
    const showSnackbar = inject('showSnackbar')

    const loadDashboardData = async () => {
      loading.value = true
      try {
        const [statsData, ordersData] = await Promise.all([
          apiService.getDashboardStats(),
          apiService.getOrders()
        ])
        
        stats.value = statsData
        recentOrders.value = ordersData.slice(0, 5) // Последние 5 заказов
        
      } catch (error) {
        console.error('Ошибка загрузки данных:', error)
        showSnackbar('Ошибка загрузки данных дашборда', 'error')
      } finally {
        loading.value = false
      }
    }

    const formatMoney = (amount) => {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
      }).format(amount)
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Неизвестно'
      return new Date(dateString).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getStatusColor = (status) => {
      const colors = {
        pending: 'warning',
        confirmed: 'info',
        completed: 'success',
        cancelled: 'error'
      }
      return colors[status] || 'grey'
    }

    const getStatusText = (status) => {
      const texts = {
        pending: 'В ожидании',
        confirmed: 'Подтвержден',
        completed: 'Завершен',
        cancelled: 'Отменен'
      }
      return texts[status] || status
    }

    onMounted(() => {
      loadDashboardData()
    })

    return {
      stats,
      recentOrders,
      loading,
      formatMoney,
      formatDate,
      getStatusColor,
      getStatusText
    }
  }
}
</script>

<style scoped>
.v-card {
  height: 100%;
}
</style> 