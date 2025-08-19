<template>
  <div>
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold mb-2">🛒 Заказы</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Управление заказами пользователей</p>
      </v-col>
    </v-row>

    <!-- Фильтры -->
    <v-row class="mb-4">
      <v-col cols="12" md="4">
        <v-select
          v-model="statusFilter"
          :items="statusOptions"
          label="Фильтр по статусу"
          variant="outlined"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-btn color="primary" @click="loadOrders" :loading="loading">
          <v-icon class="mr-2">mdi-refresh</v-icon>
          Обновить
        </v-btn>
      </v-col>
    </v-row>

    <!-- Таблица заказов -->
    <v-card>
      <v-card-title>
        <v-icon class="mr-2">mdi-cart</v-icon>
        Список заказов ({{ filteredOrders.length }})
      </v-card-title>
      
      <v-data-table
        :headers="headers"
        :items="filteredOrders"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.user="{ item }">
          {{ item.user?.name || 'Неизвестен' }}
        </template>
        
        <template v-slot:item.total_amount="{ item }">
          {{ formatMoney(item.total_amount || 0) }}
        </template>
        
        <template v-slot:item.status="{ item }">
          <v-select
            :model-value="item.status"
            :items="statusOptions"
            variant="outlined"
            density="compact"
            hide-details
            @update:model-value="(value) => updateOrderStatus(item.id, value)"
          ></v-select>
        </template>
        
        <template v-slot:item.order_date="{ item }">
          {{ formatDate(item.order_date) }}
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn 
            icon="mdi-eye" 
            size="small" 
            variant="text"
            @click="viewOrder(item)"
          ></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог просмотра заказа -->
    <v-dialog v-model="viewDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-receipt</v-icon>
          Детали заказа #{{ viewedOrder?.id }}
        </v-card-title>
        
        <v-card-text v-if="viewedOrder">
          <v-row>
            <v-col cols="12" md="6">
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Заказчик</div>
                <div class="text-h6">{{ viewedOrder.user?.name || 'Неизвестен' }}</div>
              </div>
              
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Статус</div>
                <v-chip :color="getStatusColor(viewedOrder.status)" size="small">
                  {{ getStatusText(viewedOrder.status) }}
                </v-chip>
              </div>
            </v-col>
            
            <v-col cols="12" md="6">
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Общая сумма</div>
                <div class="text-h6">{{ formatMoney(viewedOrder.total_amount || 0) }}</div>
              </div>
              
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Дата заказа</div>
                <div class="text-h6">{{ formatDate(viewedOrder.order_date) }}</div>
              </div>
            </v-col>
          </v-row>
          
          <!-- Товары в заказе -->
          <v-divider class="my-4"></v-divider>
          <div class="text-h6 mb-4">Состав заказа</div>
          
          <div v-if="orderItems.length > 0">
            <v-list>
              <v-list-item v-for="item in orderItems" :key="item.product_id">
                <template v-slot:prepend>
                  <v-icon>mdi-package-variant</v-icon>
                </template>
                
                <v-list-item-title>{{ item.name }}</v-list-item-title>
                <v-list-item-subtitle>
                  Количество: {{ item.quantity }} × {{ formatMoney(item.price) }}
                </v-list-item-subtitle>
                
                <template v-slot:append>
                  <div class="text-h6">{{ formatMoney(item.total) }}</div>
                </template>
              </v-list-item>
            </v-list>
          </div>
          
          <div v-else class="text-center py-4 text-medium-emphasis">
            <v-icon size="32" class="mb-2">mdi-package-variant-closed</v-icon>
            <div>Данные о товарах недоступны</div>
          </div>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="viewDialog = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, inject } from 'vue'
import { apiService } from '../services/api.js'

export default {
  name: 'Orders',
  setup() {
    const orders = ref([])
    const loading = ref(false)
    const statusFilter = ref('')
    const viewDialog = ref(false)
    const viewedOrder = ref(null)
    const orderItems = ref([])
    const showSnackbar = inject('showSnackbar')

    const headers = [
      { title: 'ID', key: 'id', align: 'start' },
      { title: 'Заказчик', key: 'user' },
      { title: 'Сумма', key: 'total_amount' },
      { title: 'Статус', key: 'status' },
      { title: 'Дата', key: 'order_date' },
      { title: 'Действия', key: 'actions', sortable: false }
    ]

    const statusOptions = [
      { title: 'В ожидании', value: 'pending' },
      { title: 'Подтвержден', value: 'confirmed' },
      { title: 'Завершен', value: 'completed' },
      { title: 'Отменен', value: 'cancelled' }
    ]

    const filteredOrders = computed(() => {
      let filtered = orders.value

      if (statusFilter.value) {
        filtered = filtered.filter(order => order.status === statusFilter.value)
      }

      return filtered
    })

    const loadOrders = async () => {
      loading.value = true
      try {
        orders.value = await apiService.getOrders()
      } catch (error) {
        console.error('Ошибка загрузки заказов:', error)
        showSnackbar('Ошибка загрузки заказов', 'error')
      } finally {
        loading.value = false
      }
    }

    const updateOrderStatus = async (orderId, status) => {
      try {
        await apiService.updateOrderStatus(orderId, status)
        showSnackbar('Статус заказа обновлен', 'success')
        await loadOrders()
      } catch (error) {
        console.error('Ошибка обновления статуса:', error)
        showSnackbar('Ошибка обновления статуса заказа', 'error')
      }
    }

    const viewOrder = (order) => {
      viewedOrder.value = order
      
      // Парсим товары из JSON данных заказа
      try {
        if (order.items && typeof order.items === 'object') {
          orderItems.value = order.items.items || []
        } else {
          orderItems.value = []
        }
      } catch (error) {
        console.error('Ошибка парсинга данных заказа:', error)
        orderItems.value = []
      }
      
      viewDialog.value = true
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

    const formatMoney = (amount) => {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
      }).format(amount)
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
      loadOrders()
    })

    return {
      orders,
      filteredOrders,
      loading,
      statusFilter,
      viewDialog,
      viewedOrder,
      orderItems,
      headers,
      statusOptions,
      loadOrders,
      updateOrderStatus,
      viewOrder,
      formatDate,
      formatMoney,
      getStatusColor,
      getStatusText
    }
  }
}
</script> 