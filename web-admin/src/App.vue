<template>
  <v-app>
    <!-- Навигация только для админки -->
    <template v-if="isAdminRoute">
      <v-navigation-drawer v-model="drawer" app>
        <v-list>
          <v-list-item prepend-icon="mdi-view-dashboard" title="Дашборд" to="/admin"></v-list-item>
          <v-list-item prepend-icon="mdi-account-group" title="Пользователи" to="/admin/users"></v-list-item>
          <v-list-item prepend-icon="mdi-package-variant" title="Продукты" to="/admin/products"></v-list-item>
          <v-list-item prepend-icon="mdi-cart" title="Заказы" to="/admin/orders"></v-list-item>
          <v-list-item prepend-icon="mdi-bell" title="Уведомления" to="/admin/notifications"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-app-bar app>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        <v-toolbar-title>Kate Bot - Админ панель</v-toolbar-title>
        <v-spacer></v-spacer>
        <v-btn icon @click="logout">
          <v-icon>mdi-logout</v-icon>
        </v-btn>
      </v-app-bar>
    </template>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>

    <v-snackbar v-model="snackbar.show" :color="snackbar.color" :timeout="3000">
      {{ snackbar.text }}
    </v-snackbar>
  </v-app>
</template>

<script>
import { ref, provide, computed } from 'vue'
import { useRoute } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const route = useRoute()
    const drawer = ref(true)
    const snackbar = ref({
      show: false,
      text: '',
      color: 'success'
    })

    // Проверяем, находимся ли мы в админской части
    const isAdminRoute = computed(() => {
      return route.path.startsWith('/admin')
    })

    const showSnackbar = (text, color = 'success') => {
      snackbar.value = {
        show: true,
        text,
        color
      }
    }

    const logout = () => {
      localStorage.removeItem('admin_token')
      window.location.reload()
    }

    // Предоставляем функцию показа уведомлений для всех компонентов
    provide('showSnackbar', showSnackbar)

    return {
      drawer,
      snackbar,
      isAdminRoute,
      logout
    }
  }
}
</script>

<style>
.v-application {
  font-family: 'Roboto', sans-serif !important;
}
</style> 