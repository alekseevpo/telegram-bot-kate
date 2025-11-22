import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import '@mdi/font/css/materialdesignicons.css'
import 'vuetify/styles'

const vuetify = createVuetify({
  components,
  directives,
  theme: {
    defaultTheme: 'light',
    themes: {
      light: {
        colors: {
          primary: '#6366F1',      // Современный индиго
          secondary: '#8B5CF6',    // Фиолетовый
          accent: '#EC4899',       // Розовый акцент
          error: '#EF4444',
          info: '#3B82F6',
          success: '#10B981',
          warning: '#F59E0B',
          background: '#FFFFFF',
          surface: '#F9FAFB',
        }
      },
      dark: {
        colors: {
          primary: '#818CF8',
          secondary: '#A78BFA',
          accent: '#F472B6',
          background: '#111827',
          surface: '#1F2937',
        }
      }
    }
  },
  defaults: {
    VBtn: {
      rounded: 'lg',
      elevation: 0,
    },
    VCard: {
      rounded: 'lg',
      elevation: 2,
    },
  }
})

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app') 