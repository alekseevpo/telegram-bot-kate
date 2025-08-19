<template>
  <div>
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold mb-2">🔔 Уведомления</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Управление уведомлениями и рассылками</p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" @click="createNotification" prepend-icon="mdi-plus">
          Создать уведомление
        </v-btn>
      </v-col>
    </v-row>

    <!-- Таблица уведомлений -->
    <v-card>
      <v-card-title>
        <v-icon class="mr-2">mdi-bell</v-icon>
        История уведомлений ({{ notifications.length }})
      </v-card-title>
      
      <v-data-table
        :headers="headers"
        :items="notifications"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.message="{ item }">
          <div class="text-truncate" style="max-width: 300px;">
            {{ item.message }}
          </div>
        </template>
        
        <template v-slot:item.target_audience="{ item }">
          <v-chip size="small" color="info">
            {{ getAudienceText(item.target_audience) }}
          </v-chip>
        </template>
        
        <template v-slot:item.send_time="{ item }">
          {{ formatDate(item.send_time) }}
        </template>
        
        <template v-slot:item.status="{ item }">
          <v-chip :color="getNotificationStatusColor(item)" size="small">
            {{ getNotificationStatusText(item) }}
          </v-chip>
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn 
            icon="mdi-eye" 
            size="small" 
            variant="text"
            @click="viewNotification(item)"
          ></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог создания уведомления -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-bell-plus</v-icon>
          Создать уведомление
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form">
            <v-textarea
              v-model="newNotification.message"
              label="Текст уведомления"
              variant="outlined"
              rows="4"
              required
              counter="1000"
              class="mb-4"
            ></v-textarea>
            
            <v-select
              v-model="newNotification.target_audience"
              :items="audienceOptions"
              label="Целевая аудитория"
              variant="outlined"
              class="mb-4"
            ></v-select>
            
            <v-text-field
              v-model="newNotification.send_time"
              label="Время отправки (оставьте пустым для немедленной отправки)"
              type="datetime-local"
              variant="outlined"
              hint="Формат: ГГГГ-ММ-ДД ЧЧ:ММ"
            ></v-text-field>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveNotification" :loading="saving">
            Отправить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог просмотра уведомления -->
    <v-dialog v-model="viewDialog" max-width="500px">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">mdi-bell</v-icon>
          Детали уведомления
        </v-card-title>
        
        <v-card-text v-if="viewedNotification">
          <div class="mb-4">
            <div class="text-caption text-medium-emphasis">Сообщение</div>
            <div class="text-body-1">{{ viewedNotification.message }}</div>
          </div>
          
          <div class="mb-4">
            <div class="text-caption text-medium-emphasis">Целевая аудитория</div>
            <v-chip size="small" color="info">
              {{ getAudienceText(viewedNotification.target_audience) }}
            </v-chip>
          </div>
          
          <div class="mb-4">
            <div class="text-caption text-medium-emphasis">Время отправки</div>
            <div class="text-body-1">{{ formatDate(viewedNotification.send_time) }}</div>
          </div>
          
          <div class="mb-4">
            <div class="text-caption text-medium-emphasis">Статус</div>
            <v-chip :color="getNotificationStatusColor(viewedNotification)" size="small">
              {{ getNotificationStatusText(viewedNotification) }}
            </v-chip>
          </div>
          
          <div class="mb-4">
            <div class="text-caption text-medium-emphasis">Дата создания</div>
            <div class="text-body-1">{{ formatDate(viewedNotification.created_at) }}</div>
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
import { ref, onMounted, inject } from 'vue'
import { apiService } from '../services/api.js'

export default {
  name: 'Notifications',
  setup() {
    const notifications = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const dialog = ref(false)
    const viewDialog = ref(false)
    const viewedNotification = ref(null)
    const newNotification = ref({
      message: '',
      target_audience: 'all',
      send_time: ''
    })
    const showSnackbar = inject('showSnackbar')

    const headers = [
      { title: 'ID', key: 'id', align: 'start' },
      { title: 'Сообщение', key: 'message' },
      { title: 'Аудитория', key: 'target_audience' },
      { title: 'Время отправки', key: 'send_time' },
      { title: 'Статус', key: 'status' },
      { title: 'Действия', key: 'actions', sortable: false }
    ]

    const audienceOptions = [
      { title: 'Все пользователи', value: 'all' },
      { title: 'Новые пользователи', value: 'new' },
      { title: 'Активные пользователи', value: 'active' },
      { title: 'Завершившие регистрацию', value: 'completed' }
    ]

    const loadNotifications = async () => {
      loading.value = true
      try {
        notifications.value = await apiService.getNotifications()
      } catch (error) {
        console.error('Ошибка загрузки уведомлений:', error)
        showSnackbar('Ошибка загрузки уведомлений', 'error')
      } finally {
        loading.value = false
      }
    }

    const createNotification = () => {
      newNotification.value = {
        message: '',
        target_audience: 'all',
        send_time: ''
      }
      dialog.value = true
    }

    const saveNotification = async () => {
      if (!newNotification.value.message.trim()) {
        showSnackbar('Введите текст уведомления', 'error')
        return
      }

      saving.value = true
      try {
        await apiService.createNotification(newNotification.value)
        showSnackbar('Уведомление создано и отправлено', 'success')
        dialog.value = false
        await loadNotifications()
      } catch (error) {
        console.error('Ошибка создания уведомления:', error)
        showSnackbar('Ошибка создания уведомления', 'error')
      } finally {
        saving.value = false
      }
    }

    const viewNotification = (notification) => {
      viewedNotification.value = notification
      viewDialog.value = true
    }

    const formatDate = (dateString) => {
      if (!dateString) return 'Не указано'
      return new Date(dateString).toLocaleDateString('ru-RU', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }

    const getAudienceText = (audience) => {
      const texts = {
        all: 'Все пользователи',
        new: 'Новые пользователи',
        active: 'Активные пользователи',
        completed: 'Завершившие регистрацию'
      }
      return texts[audience] || audience
    }

    const getNotificationStatusColor = (notification) => {
      const now = new Date()
      const sendTime = new Date(notification.send_time)
      
      if (notification.sent) {
        return 'success'
      } else if (sendTime > now) {
        return 'warning'
      } else {
        return 'info'
      }
    }

    const getNotificationStatusText = (notification) => {
      const now = new Date()
      const sendTime = new Date(notification.send_time)
      
      if (notification.sent) {
        return 'Отправлено'
      } else if (sendTime > now) {
        return 'Запланировано'
      } else {
        return 'Ожидает отправки'
      }
    }

    onMounted(() => {
      loadNotifications()
    })

    return {
      notifications,
      loading,
      saving,
      dialog,
      viewDialog,
      viewedNotification,
      newNotification,
      headers,
      audienceOptions,
      loadNotifications,
      createNotification,
      saveNotification,
      viewNotification,
      formatDate,
      getAudienceText,
      getNotificationStatusColor,
      getNotificationStatusText
    }
  }
}
</script> 