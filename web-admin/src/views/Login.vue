<template>
  <v-container class="fill-height" fluid>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card elevation="12" rounded="lg">
          <v-card-title class="text-center py-6">
            <v-icon size="48" color="primary" class="mb-4">mdi-robot</v-icon>
            <div class="text-h4 font-weight-bold">Kate Bot</div>
            <div class="text-subtitle-1 text-medium-emphasis">Админ панель</div>
          </v-card-title>
          
          <v-card-text class="px-6">
            <v-form @submit.prevent="login" ref="form">
              <v-text-field
                v-model="adminId"
                label="ID Администратора"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                required
                :rules="[rules.required]"
                class="mb-4"
              ></v-text-field>
              
              <v-btn
                type="submit"
                color="primary"
                size="large"
                variant="flat"
                block
                :loading="loading"
                class="mb-4"
              >
                Войти
              </v-btn>
            </v-form>
            
            <v-alert v-if="error" type="error" variant="outlined" class="mb-4">
              {{ error }}
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { apiService } from '../services/api.js'

export default {
  name: 'Login',
  setup() {
    const router = useRouter()
    const adminId = ref('')
    const loading = ref(false)
    const error = ref('')
    
    const rules = {
      required: value => !!value || 'Поле обязательно для заполнения'
    }
    
    const login = async () => {
      if (!adminId.value) {
        error.value = 'Введите ID администратора'
        return
      }
      
      loading.value = true
      error.value = ''
      
      try {
        await apiService.login(adminId.value)
        router.push('/')
      } catch (err) {
        error.value = 'Ошибка авторизации'
      } finally {
        loading.value = false
      }
    }
    
    return {
      adminId,
      loading,
      error,
      rules,
      login
    }
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.v-card {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.95) !important;
}
</style> 