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
          primary: '#8B5FBF',      // Теплый фиолетовый
          secondary: '#D4A5D4',    // Нежный розово-фиолетовый
          accent: '#FFA07A',       // Теплый лососевый
          error: '#EF4444',
          info: '#7EC8E3',
          success: '#81C784',
          warning: '#FFB74D',
          background: '#FFFFFF',
          surface: '#FAF9F6',
        }
      },
      dark: {
        colors: {
          primary: '#A78BFA',
          secondary: '#D4A5D4',
          accent: '#FFA07A',
          background: '#111827',
          surface: '#1F2937',
        }
      }
    }
  },
  defaults: {
    VBtn: {
      rounded: 'xl',
      elevation: 0,
      style: 'text-transform: none; letter-spacing: 0.5px;',
    },
    VCard: {
      rounded: 'xl',
      elevation: 0,
    },
  }
})

const app = createApp(App)
app.use(router)
app.use(vuetify)
app.mount('#app') 