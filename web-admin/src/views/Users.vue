<template>
  <div>
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold mb-2">👥 Пользователи</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Управление пользователями бота</p>
      </v-col>
    </v-row>

    <!-- Поиск и фильтры -->
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="search"
          prepend-inner-icon="mdi-magnify"
          label="Поиск пользователей"
          variant="outlined"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="stageFilter"
          :items="stageOptions"
          label="Фильтр по этапу"
          variant="outlined"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="3">
        <v-btn color="primary" @click="loadUsers" :loading="loading">
          <v-icon class="mr-2">mdi-refresh</v-icon>
          Обновить
        </v-btn>
      </v-col>
    </v-row>

    <!-- Таблица пользователей -->
    <v-card>
      <v-card-title>
        <v-icon class="mr-2">mdi-account-group</v-icon>
        Список пользователей ({{ filteredUsers.length }})
      </v-card-title>
      
      <v-data-table
        :headers="headers"
        :items="filteredUsers"
        :loading="loading"
        :search="search"
        class="elevation-1"
      >
        <template v-slot:item.gender="{ item }">
          <v-chip :color="item.gender === 'male' ? 'blue' : 'pink'" size="small">
            {{ item.gender === 'male' ? 'Мужской' : 'Женский' }}
          </v-chip>
        </template>
        
        <template v-slot:item.stage="{ item }">
          <v-chip :color="getStageColor(item.stage)" size="small">
            {{ getStageText(item.stage) }}
          </v-chip>
        </template>
        
        <template v-slot:item.registration_date="{ item }">
          {{ formatDate(item.registration_date) }}
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn 
            icon="mdi-pencil" 
            size="small" 
            variant="text"
            @click="editUser(item)"
          ></v-btn>
          <v-btn 
            icon="mdi-eye" 
            size="small" 
            variant="text"
            @click="viewUser(item)"
          ></v-btn>
        </template>
        
        <template v-slot:no-data>
          <div class="text-center py-8">
            <v-icon size="48" class="mb-4 text-medium-emphasis">mdi-account-off</v-icon>
            <div class="text-medium-emphasis">Пользователи не найдены</div>
          </div>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог редактирования пользователя -->
    <v-dialog v-model="editDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-account-edit</v-icon>
          Редактировать пользователя
        </v-card-title>
        
        <v-card-text>
          <v-form ref="editForm">
            <v-text-field
              v-model="editedUser.name"
              label="Имя"
              variant="outlined"
              class="mb-4"
            ></v-text-field>
            
            <v-select
              v-model="editedUser.gender"
              :items="genderOptions"
              label="Пол"
              variant="outlined"
              class="mb-4"
            ></v-select>
            
            <v-select
              v-model="editedUser.stage"
              :items="stageOptions"
              label="Этап"
              variant="outlined"
              class="mb-4"
            ></v-select>
            
            <v-text-field
              v-model="editedUser.phone"
              label="Телефон"
              variant="outlined"
            ></v-text-field>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="editDialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveUser" :loading="saving">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог просмотра пользователя -->
    <v-dialog v-model="viewDialog" max-width="600px">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-account</v-icon>
          Профиль пользователя
        </v-card-title>
        
        <v-card-text>
          <v-row v-if="viewedUser">
            <v-col cols="12" md="6">
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Имя</div>
                <div class="text-h6">{{ viewedUser.name || 'Не указано' }}</div>
              </div>
              
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Пол</div>
                <v-chip :color="viewedUser.gender === 'male' ? 'blue' : 'pink'" size="small">
                  {{ viewedUser.gender === 'male' ? 'Мужской' : 'Женский' }}
                </v-chip>
              </div>
              
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Этап</div>
                <v-chip :color="getStageColor(viewedUser.stage)" size="small">
                  {{ getStageText(viewedUser.stage) }}
                </v-chip>
              </div>
            </v-col>
            
            <v-col cols="12" md="6">
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Telegram ID</div>
                <div class="text-h6">{{ viewedUser.user_id }}</div>
              </div>
              
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Телефон</div>
                <div class="text-h6">{{ viewedUser.phone || 'Не указан' }}</div>
              </div>
              
              <div class="mb-4">
                <div class="text-caption text-medium-emphasis">Дата регистрации</div>
                <div class="text-h6">{{ formatDate(viewedUser.registration_date) }}</div>
              </div>
            </v-col>
          </v-row>
          
          <!-- Заказы пользователя -->
          <v-divider class="my-4"></v-divider>
          <div class="text-h6 mb-4">Заказы пользователя</div>
          
          <v-table v-if="userOrders.length > 0">
            <thead>
              <tr>
                <th>ID</th>
                <th>Сумма</th>
                <th>Статус</th>
                <th>Дата</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="order in userOrders" :key="order.id">
                <td>{{ order.id }}</td>
                <td>{{ formatMoney(order.total_amount || 0) }}</td>
                <td>
                  <v-chip :color="getStatusColor(order.status)" size="small">
                    {{ getStatusText(order.status) }}
                  </v-chip>
                </td>
                <td>{{ formatDate(order.order_date) }}</td>
              </tr>
            </tbody>
          </v-table>
          
          <div v-else class="text-center py-4 text-medium-emphasis">
            <v-icon size="32" class="mb-2">mdi-cart-off</v-icon>
            <div>Заказов нет</div>
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
  name: 'Users',
  setup() {
    const users = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const search = ref('')
    const stageFilter = ref('')
    const editDialog = ref(false)
    const viewDialog = ref(false)
    const editedUser = ref({})
    const viewedUser = ref(null)
    const userOrders = ref([])
    const showSnackbar = inject('showSnackbar')

    const headers = [
      { title: 'ID', key: 'user_id', align: 'start' },
      { title: 'Имя', key: 'name' },
      { title: 'Пол', key: 'gender' },
      { title: 'Этап', key: 'stage' },
      { title: 'Телефон', key: 'phone' },
      { title: 'Дата регистрации', key: 'registration_date' },
      { title: 'Действия', key: 'actions', sortable: false }
    ]

    const genderOptions = [
      { title: 'Мужской', value: 'male' },
      { title: 'Женский', value: 'female' }
    ]

    const stageOptions = [
      { title: 'Новый', value: 'new' },
      { title: 'Знакомство', value: 'greeting' },
      { title: 'Получил материалы', value: 'materials_sent' },
      { title: 'Указал контакты', value: 'contacts_provided' },
      { title: 'Завершенный', value: 'completed' }
    ]

    const filteredUsers = computed(() => {
      let filtered = users.value

      if (stageFilter.value) {
        filtered = filtered.filter(user => user.stage === stageFilter.value)
      }

      return filtered
    })

    const loadUsers = async () => {
      loading.value = true
      try {
        users.value = await apiService.getUsers()
      } catch (error) {
        console.error('Ошибка загрузки пользователей:', error)
        showSnackbar('Ошибка загрузки пользователей', 'error')
      } finally {
        loading.value = false
      }
    }

    const editUser = (user) => {
      editedUser.value = { ...user }
      editDialog.value = true
    }

    const viewUser = async (user) => {
      try {
        const userData = await apiService.getUser(user.user_id)
        viewedUser.value = userData.user
        userOrders.value = userData.orders || []
        viewDialog.value = true
      } catch (error) {
        console.error('Ошибка загрузки пользователя:', error)
        showSnackbar('Ошибка загрузки данных пользователя', 'error')
      }
    }

    const saveUser = async () => {
      saving.value = true
      try {
        await apiService.updateUser(editedUser.value.user_id, {
          name: editedUser.value.name,
          gender: editedUser.value.gender,
          stage: editedUser.value.stage,
          phone: editedUser.value.phone
        })
        
        showSnackbar('Пользователь успешно обновлен', 'success')
        editDialog.value = false
        await loadUsers()
      } catch (error) {
        console.error('Ошибка сохранения пользователя:', error)
        showSnackbar('Ошибка сохранения пользователя', 'error')
      } finally {
        saving.value = false
      }
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

    const getStageColor = (stage) => {
      const colors = {
        new: 'grey',
        greeting: 'blue',
        materials_sent: 'orange',
        contacts_provided: 'purple',
        completed: 'green'
      }
      return colors[stage] || 'grey'
    }

    const getStageText = (stage) => {
      const texts = {
        new: 'Новый',
        greeting: 'Знакомство',
        materials_sent: 'Получил материалы',
        contacts_provided: 'Указал контакты',
        completed: 'Завершенный'
      }
      return texts[stage] || stage
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
      loadUsers()
    })

    return {
      users,
      filteredUsers,
      loading,
      saving,
      search,
      stageFilter,
      editDialog,
      viewDialog,
      editedUser,
      viewedUser,
      userOrders,
      headers,
      genderOptions,
      stageOptions,
      loadUsers,
      editUser,
      viewUser,
      saveUser,
      formatDate,
      formatMoney,
      getStageColor,
      getStageText,
      getStatusColor,
      getStatusText
    }
  }
}
</script>

<style scoped>
.v-data-table {
  background: transparent;
}
</style> 