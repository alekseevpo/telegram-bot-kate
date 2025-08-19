<template>
  <div>
    <!-- Hero секция -->
    <v-container fluid class="hero-section pa-0">
      <v-row align="center" justify="center" class="hero-content">
        <v-col cols="12" md="8" class="text-center">
          <h1 class="text-h2 font-weight-bold text-white mb-4">
            Добро пожаловать в Kate Bot
          </h1>
          <p class="text-h5 text-white mb-6">
            Профессиональные услуги и качественные продукты для вашего развития
          </p>
          <v-btn 
            size="x-large" 
            color="primary" 
            variant="flat"
            href="https://t.me/kate202_bot"
            target="_blank"
            prepend-icon="mdi-telegram"
          >
            Начать в Telegram
          </v-btn>
        </v-col>
      </v-row>
    </v-container>

    <!-- О нас -->
    <v-container class="py-16">
      <v-row align="center">
        <v-col cols="12" md="6">
          <h2 class="text-h3 font-weight-bold mb-6">О нас</h2>
          <p class="text-body-1 text-medium-emphasis mb-4">
            Мы специализируемся на предоставлении высококачественных услуг и продуктов, 
            которые помогут вам достичь ваших целей и улучшить качество жизни.
          </p>
          <p class="text-body-1 text-medium-emphasis mb-6">
            Наша команда экспертов готова помочь вам на каждом этапе вашего пути к успеху.
          </p>
          <v-btn 
            color="primary" 
            variant="outlined" 
            size="large"
            @click="scrollToProducts"
          >
            Наши услуги
          </v-btn>
        </v-col>
        <v-col cols="12" md="6" class="text-center">
          <v-icon size="120" color="primary" class="mb-4">mdi-robot</v-icon>
          <div class="text-h4 font-weight-bold text-primary">Kate Bot</div>
          <div class="text-subtitle-1 text-medium-emphasis">Ваш надежный помощник</div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Преимущества -->
    <v-container class="py-16 bg-grey-lighten-5">
      <v-row class="text-center mb-12">
        <v-col>
          <h2 class="text-h3 font-weight-bold mb-4">Почему выбирают нас</h2>
          <p class="text-body-1 text-medium-emphasis">
            Мы предлагаем уникальные преимущества, которые выделяют нас среди конкурентов
          </p>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12" md="4" class="text-center">
          <v-icon size="64" color="primary" class="mb-4">mdi-clock-fast</v-icon>
          <h3 class="text-h5 font-weight-bold mb-3">Быстро и качественно</h3>
          <p class="text-body-2 text-medium-emphasis">
            Получите результат в кратчайшие сроки без потери качества
          </p>
        </v-col>
        
        <v-col cols="12" md="4" class="text-center">
          <v-icon size="64" color="primary" class="mb-4">mdi-account-group</v-icon>
          <h3 class="text-h5 font-weight-bold mb-3">Персональный подход</h3>
          <p class="text-body-2 text-medium-emphasis">
            Индивидуальные решения для каждого клиента
          </p>
        </v-col>
        
        <v-col cols="12" md="4" class="text-center">
          <v-icon size="64" color="primary" class="mb-4">mdi-shield-check</v-icon>
          <h3 class="text-h5 font-weight-bold mb-3">Гарантия качества</h3>
          <p class="text-body-2 text-medium-emphasis">
            Мы гарантируем высокое качество всех наших услуг
          </p>
        </v-col>
      </v-row>
    </v-container>

    <!-- Каталог продуктов -->
    <v-container class="py-16" id="products">
      <v-row class="text-center mb-12">
        <v-col>
          <h2 class="text-h3 font-weight-bold mb-4">Наши продукты и услуги</h2>
          <p class="text-body-1 text-medium-emphasis">
            Выберите то, что подходит именно вам
          </p>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col 
          v-for="product in products" 
          :key="product.id" 
          cols="12" 
          sm="6" 
          md="4" 
          class="mb-6"
        >
          <v-card 
            class="product-card h-100" 
            elevation="4" 
            hover
          >
            <v-card-title class="text-h6 font-weight-bold text-center pa-4">
              {{ product.name }}
            </v-card-title>
            
            <v-card-text class="text-center pa-4">
              <p class="text-body-2 text-medium-emphasis mb-4">
                {{ product.description }}
              </p>
              
              <div class="text-h5 font-weight-bold text-primary mb-4">
                {{ formatMoney(product.price) }}
              </div>
              
              <v-btn 
                color="primary" 
                variant="flat" 
                block
                href="https://t.me/your_bot_username"
                target="_blank"
                prepend-icon="mdi-cart"
              >
                Заказать
              </v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-container>

    <!-- Как это работает -->
    <v-container class="py-16 bg-grey-lighten-5">
      <v-row class="text-center mb-12">
        <v-col>
          <h2 class="text-h3 font-weight-bold mb-4">Как это работает</h2>
          <p class="text-body-1 text-medium-emphasis">
            Простой процесс получения наших услуг
          </p>
        </v-col>
      </v-row>
      
      <v-row>
        <v-col cols="12" md="3" class="text-center">
          <div class="step-circle mb-4">1</div>
          <h3 class="text-h6 font-weight-bold mb-3">Напишите боту</h3>
          <p class="text-body-2 text-medium-emphasis">
            Отправьте сообщение в Telegram бот
          </p>
        </v-col>
        
        <v-col cols="12" md="3" class="text-center">
          <div class="step-circle mb-4">2</div>
          <h3 class="text-h6 font-weight-bold mb-3">Выберите услугу</h3>
          <p class="text-body-2 text-medium-emphasis">
            Изучите каталог и выберите нужную услугу
          </p>
        </v-col>
        
        <v-col cols="12" md="3" class="text-center">
          <div class="step-circle mb-4">3</div>
          <h3 class="text-h6 font-weight-bold mb-3">Оплатите</h3>
          <p class="text-body-2 text-medium-emphasis">
            Безопасная оплата картой или другими способами
          </p>
        </v-col>
        
        <v-col cols="12" md="3" class="text-center">
          <div class="step-circle mb-4">4</div>
          <h3 class="text-h6 font-weight-bold mb-3">Получите результат</h3>
          <p class="text-body-2 text-medium-emphasis">
            Быстрое получение заказанной услуги
          </p>
        </v-col>
      </v-row>
    </v-container>

    <!-- Контакты -->
    <v-container class="py-16">
      <v-row align="center">
        <v-col cols="12" md="6">
          <h2 class="text-h3 font-weight-bold mb-6">Свяжитесь с нами</h2>
          <p class="text-body-1 text-medium-emphasis mb-4">
            У вас есть вопросы? Мы готовы помочь!
          </p>
          
          <div class="d-flex align-center mb-4">
            <v-icon color="primary" class="mr-3">mdi-telegram</v-icon>
            <span class="text-body-1">@kate202_bot</span>
          </div>
          
          <div class="d-flex align-center mb-4">
            <v-icon color="primary" class="mr-3">mdi-email</v-icon>
            <span class="text-body-1">info@katebot.com</span>
          </div>
          
          <div class="d-flex align-center mb-6">
            <v-icon color="primary" class="mr-3">mdi-clock</v-icon>
            <span class="text-body-1">24/7 поддержка</span>
          </div>
          
          <v-btn 
            color="primary" 
            variant="flat" 
            size="large"
            href="https://t.me/kate202_bot"
            target="_blank"
            prepend-icon="mdi-telegram"
          >
            Написать в Telegram
          </v-btn>
        </v-col>
        
        <v-col cols="12" md="6" class="text-center">
          <v-icon size="120" color="primary" class="mb-4">mdi-message-text</v-icon>
          <div class="text-h4 font-weight-bold text-primary">Готовы помочь</div>
          <div class="text-subtitle-1 text-medium-emphasis">Ответим на все ваши вопросы</div>
        </v-col>
      </v-row>
    </v-container>

    <!-- Футер с скрытой ссылкой на админку -->
    <v-footer class="bg-grey-darken-4 text-white">
      <v-container>
        <v-row align="center" justify="space-between">
          <v-col cols="12" md="6">
            <div class="text-body-2">
              © 2025 Kate Bot. Все права защищены.
            </div>
          </v-col>
          
          <v-col cols="12" md="6" class="text-right">
            <a 
              href="/admin" 
              class="text-caption text-grey-lighten-1 text-decoration-none"
              style="font-size: 10px; opacity: 0.3;"
            >
              Админ панель
            </a>
          </v-col>
        </v-row>
      </v-container>
    </v-footer>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { apiService } from '../services/api.js'

export default {
  name: 'Home',
  setup() {
    const products = ref([])

    const loadProducts = async () => {
      try {
        // Загружаем продукты через API сервис
        products.value = await apiService.getPublicProducts()
      } catch (error) {
        console.error('Ошибка загрузки продуктов:', error)
        // Если API недоступен, показываем демо продукты
        products.value = [
          {
            id: 1,
            name: 'Базовый курс',
            description: 'Полный курс по основам метода работы. Идеально для начинающих.',
            price: 5000
          },
          {
            id: 2,
            name: 'Продвинутый курс',
            description: 'Углубленное изучение продвинутых техник для опытных пользователей.',
            price: 10000
          },
          {
            id: 3,
            name: 'Индивидуальная консультация',
            description: 'Персональная консультация 1-на-1 с экспертом.',
            price: 3000
          },
          {
            id: 4,
            name: 'Групповой мастер-класс',
            description: 'Участие в групповом мастер-классе с другими участниками.',
            price: 1500
          }
        ]
      }
    }

    const formatMoney = (amount) => {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
      }).format(amount)
    }

    const scrollToProducts = () => {
      document.getElementById('products').scrollIntoView({ 
        behavior: 'smooth' 
      })
    }

    onMounted(() => {
      loadProducts()
    })

    return {
      products,
      formatMoney,
      scrollToProducts
    }
  }
}
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 80vh;
  display: flex;
  align-items: center;
}

.hero-content {
  min-height: 80vh;
}

.step-circle {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  font-weight: bold;
  margin: 0 auto;
}

.product-card {
  transition: transform 0.3s ease;
}

.product-card:hover {
  transform: translateY(-5px);
}

.text-decoration-none {
  text-decoration: none;
}
</style> 