<template>
  <div class="home-page">
    <!-- Hero секция с градиентом и анимацией -->
    <section class="hero-section">
      <div class="hero-background"></div>
      <v-container fluid class="hero-content px-4">
        <v-row align="center" justify="center">
          <v-col cols="12" md="10" lg="8" class="text-center">
            <div class="hero-badge mb-6" data-aos="fade-down">
              <v-chip color="primary" variant="flat" size="small" class="px-4">
                🎉 Новинка: Бесплатная консультация
              </v-chip>
            </div>
            
            <h1 class="hero-title mb-6" data-aos="fade-up">
              Екатерина - кризисный <span class="gradient-text">целитель</span>
            </h1>
            
            <p class="hero-subtitle mb-8" data-aos="fade-up" data-aos-delay="100">
              Профессиональная психологическая помощь и поддержка в трудные моменты жизни.<br/>
              Вместе мы найдем выход из любой ситуации
            </p>
            
            <div class="hero-actions" data-aos="fade-up" data-aos-delay="200">
              <v-btn 
                size="x-large" 
                color="primary" 
                variant="flat"
                href="https://t.me/kate202_bot"
                target="_blank"
                class="mr-4 mb-3 telegram-btn"
                prepend-icon="mdi-telegram"
              >
                Начать в Telegram
              </v-btn>
              <v-btn 
                size="x-large" 
                variant="flat"
                color="white"
                class="mb-3 catalog-btn"
                @click="scrollToProducts"
              >
                Смотреть каталог
              </v-btn>
            </div>
            
            <!-- Статистика -->
            <v-row class="mt-12 stats-row" data-aos="fade-up" data-aos-delay="300">
              <v-col cols="12" sm="4">
                <div class="stat-item">
                  <div class="stat-number">1000+</div>
                  <div class="stat-label">Довольных клиентов</div>
                </div>
              </v-col>
              <v-col cols="12" sm="4">
                <div class="stat-item">
                  <div class="stat-number">4.9/5</div>
                  <div class="stat-label">Средняя оценка</div>
                </div>
              </v-col>
              <v-col cols="12" sm="4">
                <div class="stat-item">
                  <div class="stat-number">24/7</div>
                  <div class="stat-label">Поддержка</div>
                </div>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
      
      <!-- Плавный переход -->
      <div class="hero-transition"></div>
    </section>

    <!-- О нас -->
    <section class="about-section section-padding">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" data-aos="fade-right">
            <div class="about-content">
              <span class="section-label mb-3 d-block">О ЦЕЛИТЕЛЕ</span>
              <h2 class="section-title mb-4">
                Помощь в преодолении жизненных кризисов
              </h2>
              <p class="section-text mb-4">
                Я - Екатерина, кризисный целитель с многолетним опытом работы. 
                Помогаю людям находить внутренние силы и ресурсы для преодоления трудных жизненных ситуаций.
              </p>
              <p class="section-text mb-6">
                Мой подход сочетает современные психологические методики с глубоким пониманием 
                человеческой природы. Я создаю безопасное пространство для вашего исцеления.
              </p>
              
              <div class="feature-list mb-6">
                <div class="feature-item">
                  <v-icon color="success" size="small">mdi-check-circle</v-icon>
                  <span>Конфиденциальность и безопасность</span>
                </div>
                <div class="feature-item">
                  <v-icon color="success" size="small">mdi-check-circle</v-icon>
                  <span>Индивидуальный подход</span>
                </div>
                <div class="feature-item">
                  <v-icon color="success" size="small">mdi-check-circle</v-icon>
                  <span>Поддержка 24/7</span>
                </div>
              </div>
              
              <v-btn 
                color="primary" 
                variant="flat" 
                size="large"
                @click="scrollToProducts"
                prepend-icon="mdi-arrow-right"
              >
                Наши услуги
              </v-btn>
            </div>
          </v-col>
          
          <v-col cols="12" md="6" class="text-center" data-aos="fade-left">
            <div class="about-image-wrapper">
              <div class="floating-card floating-card-1">
                <v-icon size="40" color="primary">mdi-lightning-bolt</v-icon>
                <div class="floating-card-text">Быстро</div>
              </div>
              <div class="floating-card floating-card-2">
                <v-icon size="40" color="secondary">mdi-shield-check</v-icon>
                <div class="floating-card-text">Надежно</div>
              </div>
              <div class="floating-card floating-card-3">
                <v-icon size="40" color="accent">mdi-star</v-icon>
                <div class="floating-card-text">Качественно</div>
              </div>
              <v-icon size="200" color="primary" class="main-icon">mdi-hands-pray</v-icon>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Преимущества -->
    <section class="features-section section-padding">
      <v-container>
        <div class="text-center mb-12" data-aos="fade-up">
          <span class="section-label mb-3 d-inline-block">ПРЕИМУЩЕСТВА</span>
          <h2 class="section-title mb-3">Почему выбирают меня</h2>
          <p class="section-subtitle mb-0">
            Профессиональная помощь с заботой о каждом клиенте
          </p>
        </div>
        
        <v-row>
          <v-col 
            v-for="(feature, index) in features" 
            :key="index"
            cols="12" 
            md="4" 
            data-aos="fade-up"
            :data-aos-delay="index * 100"
          >
            <v-card class="feature-card h-100" hover>
              <v-card-text class="pa-8 text-center">
                <div class="feature-icon-wrapper mb-4">
                  <v-icon :color="feature.color" size="48">{{ feature.icon }}</v-icon>
                </div>
                <h3 class="text-h5 font-weight-bold mb-3">{{ feature.title }}</h3>
                <p class="text-body-2 text-medium-emphasis">
                  {{ feature.description }}
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Каталог продуктов -->
    <section class="products-section section-padding" id="products">
      <v-container>
        <div class="text-center mb-12" data-aos="fade-up">
          <span class="section-label mb-3 d-inline-block">УСЛУГИ</span>
          <h2 class="section-title mb-3">Мои услуги и программы</h2>
          <p class="section-subtitle mb-0">
            Выберите формат работы, который подходит именно вам
          </p>
        </div>
        
        <v-row v-if="products.length > 0">
          <v-col 
            v-for="(product, index) in products" 
            :key="product.id" 
            cols="12" 
            sm="6" 
            lg="3"
            data-aos="fade-up"
            :data-aos-delay="index * 100"
          >
            <v-card 
              class="product-card h-100" 
              hover
            >
              <!-- Иконка продукта -->
              <div class="product-icon-wrapper">
                <v-icon size="60" color="primary">{{ getProductIcon(index) }}</v-icon>
              </div>
              
              <v-card-title class="text-h6 font-weight-bold text-center px-4 pt-4 pb-2">
                {{ product.name }}
              </v-card-title>
              
              <v-card-text class="text-center px-4 pb-4">
                <p class="product-description text-body-2 mb-4">
                  {{ product.description }}
                </p>
                
                <div class="product-price mb-4">
                  <span class="price-amount">{{ formatMoney(product.price) }}</span>
                </div>
                
                <v-btn 
                  color="primary" 
                  variant="flat" 
                  block
                  @click="$router.push(`/product/${product.id}`)"
                  prepend-icon="mdi-information"
                  size="large"
                  class="mb-2"
                >
                  Подробнее
                </v-btn>
                
                <v-btn 
                  color="primary" 
                  variant="outlined" 
                  block
                  href="https://t.me/kate202_bot"
                  target="_blank"
                  prepend-icon="mdi-cart-outline"
                  size="large"
                >
                  Заказать
                </v-btn>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
        
        <!-- Загрузка -->
        <div v-else class="text-center py-8" data-aos="fade-up">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
          <p class="mt-4 text-medium-emphasis">Загрузка продуктов...</p>
        </div>
      </v-container>
    </section>

    <!-- Отзывы -->
    <section class="testimonials-section section-padding">
      <v-container>
        <div class="text-center mb-12" data-aos="fade-up">
          <span class="section-label mb-3 d-inline-block">ОТЗЫВЫ</span>
          <h2 class="section-title mb-3">Отзывы моих клиентов</h2>
          <p class="section-subtitle mb-0">
            Реальные истории людей, которым я помогла
          </p>
        </div>
        
        <v-row>
          <v-col 
            v-for="(testimonial, index) in testimonials" 
            :key="index"
            cols="12" 
            md="4"
            data-aos="fade-up"
            :data-aos-delay="index * 100"
          >
            <v-card class="testimonial-card h-100">
              <v-card-text class="pa-6">
                <div class="rating mb-3">
                  <v-icon 
                    v-for="i in 5" 
                    :key="i" 
                    size="small" 
                    color="warning"
                  >
                    mdi-star
                  </v-icon>
                </div>
                <p class="testimonial-text mb-4">
                  "{{ testimonial.text }}"
                </p>
                <div class="testimonial-author">
                  <div class="author-avatar">
                    {{ testimonial.name.charAt(0) }}
                  </div>
                  <div>
                    <div class="author-name">{{ testimonial.name }}</div>
                    <div class="author-role">{{ testimonial.role }}</div>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Как это работает -->
    <section class="process-section section-padding">
      <v-container>
        <div class="text-center mb-12" data-aos="fade-up">
          <span class="section-label mb-3 d-inline-block">ПРОЦЕСС</span>
          <h2 class="section-title mb-3">Как проходит работа</h2>
          <p class="section-subtitle mb-0">
            Простой и комфортный процесс начала нашего сотрудничества
          </p>
        </div>
        
        <v-row class="process-steps">
          <v-col 
            v-for="(step, index) in steps" 
            :key="index"
            cols="12" 
            sm="6" 
            lg="3"
            data-aos="zoom-in"
            :data-aos-delay="index * 100"
          >
            <div class="process-step">
              <div class="step-number">{{ index + 1 }}</div>
              <div class="step-icon">
                <v-icon size="40" color="primary">{{ step.icon }}</v-icon>
              </div>
              <h3 class="step-title">{{ step.title }}</h3>
              <p class="step-description">{{ step.description }}</p>
            </div>
            <div v-if="index < steps.length - 1" class="step-connector"></div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA секция -->
    <section class="cta-section section-padding">
      <v-container>
        <v-card class="cta-card" elevation="0" data-aos="zoom-in">
          <v-card-text class="pa-12 text-center">
            <h2 class="section-title text-white mb-4">
              Готовы начать?
            </h2>
            <p class="cta-subtitle text-white mb-8">
              Присоединяйтесь к тысячам довольных клиентов уже сегодня
            </p>
            <v-btn 
              size="x-large" 
              color="white" 
              variant="flat"
              href="https://t.me/kate202_bot"
              target="_blank"
              prepend-icon="mdi-telegram"
            >
              Начать в Telegram
            </v-btn>
          </v-card-text>
        </v-card>
      </v-container>
    </section>

    <!-- Контакты -->
    <section class="contact-section section-padding">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" data-aos="fade-right">
            <span class="section-label mb-3 d-block">КОНТАКТЫ</span>
            <h2 class="section-title mb-4">Свяжитесь со мной</h2>
            <p class="section-text mb-6">
              Готовы начать путь к изменениям? Я здесь, чтобы помочь!
              Свяжитесь со мной удобным для вас способом.
            </p>
            
            <div class="contact-info mb-8">
              <div class="contact-item">
                <div class="contact-icon">
                  <v-icon color="primary">mdi-telegram</v-icon>
                </div>
                <div>
                  <div class="contact-label">Telegram</div>
                  <div class="contact-value">@kate202_bot</div>
                </div>
              </div>
              
              <div class="contact-item">
                <div class="contact-icon">
                  <v-icon color="primary">mdi-email</v-icon>
                </div>
                <div>
                  <div class="contact-label">Email</div>
                  <div class="contact-value">info@katebot.com</div>
                </div>
              </div>
              
              <div class="contact-item">
                <div class="contact-icon">
                  <v-icon color="primary">mdi-clock</v-icon>
                </div>
                <div>
                  <div class="contact-label">Режим работы</div>
                  <div class="contact-value">24/7 поддержка</div>
                </div>
              </div>
            </div>
            
            <v-btn 
              color="primary" 
              variant="flat" 
              size="x-large"
              href="https://t.me/kate202_bot"
              target="_blank"
              prepend-icon="mdi-send"
            >
              Написать сообщение
            </v-btn>
          </v-col>
          
          <v-col cols="12" md="6" data-aos="fade-left">
            <v-card class="contact-card pa-8" elevation="4">
              <h3 class="text-h5 font-weight-bold mb-6">Быстрая связь</h3>
              <v-form @submit.prevent="sendQuickMessage">
                <v-text-field
                  v-model="quickForm.name"
                  label="Ваше имя"
                  variant="outlined"
                  prepend-inner-icon="mdi-account"
                  class="mb-4"
                ></v-text-field>
                
                <v-text-field
                  v-model="quickForm.email"
                  label="Email"
                  type="email"
                  variant="outlined"
                  prepend-inner-icon="mdi-email"
                  class="mb-4"
                ></v-text-field>
                
                <v-textarea
                  v-model="quickForm.message"
                  label="Ваше сообщение"
                  variant="outlined"
                  prepend-inner-icon="mdi-message-text"
                  rows="4"
                  class="mb-4"
                ></v-textarea>
                
                <v-btn 
                  type="submit"
                  color="primary" 
                  variant="flat" 
                  size="large"
                  block
                  prepend-icon="mdi-send"
                >
                  Отправить
                </v-btn>
              </v-form>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Футер -->
    <footer class="footer-section">
      <v-container>
        <v-row class="py-12">
          <v-col cols="12" md="4" class="mb-6">
            <div class="footer-brand mb-4">
              <v-icon size="40" color="primary">mdi-heart-pulse</v-icon>
              <span class="footer-logo">Екатерина</span>
            </div>
            <p class="footer-description">
              Кризисный целитель. Профессиональная психологическая помощь 
              и поддержка в трудные моменты жизни. С заботой о каждом.
            </p>
          </v-col>
          
          <v-col cols="12" sm="6" md="2" class="mb-6">
            <h4 class="footer-title mb-4">Продукты</h4>
            <ul class="footer-links">
              <li><a href="#products" @click.prevent="scrollToProducts">Каталог</a></li>
              <li><a href="#products">Курсы</a></li>
              <li><a href="#products">Консультации</a></li>
            </ul>
          </v-col>
          
          <v-col cols="12" sm="6" md="2" class="mb-6">
            <h4 class="footer-title mb-4">Компания</h4>
            <ul class="footer-links">
              <li><a href="#about">О нас</a></li>
              <li><a href="#contact">Контакты</a></li>
              <li><a href="/admin" style="opacity: 0.3;">Админ</a></li>
            </ul>
          </v-col>
          
          <v-col cols="12" sm="6" md="2" class="mb-6">
            <h4 class="footer-title mb-4">Поддержка</h4>
            <ul class="footer-links">
              <li><a href="https://t.me/kate202_bot" target="_blank">FAQ</a></li>
              <li><a href="https://t.me/kate202_bot" target="_blank">Помощь</a></li>
            </ul>
          </v-col>
          
          <v-col cols="12" sm="6" md="2" class="mb-6">
            <h4 class="footer-title mb-4">Соц. сети</h4>
            <div class="footer-social">
              <v-btn icon variant="text" size="small" href="https://t.me/kate202_bot" target="_blank">
                <v-icon>mdi-telegram</v-icon>
              </v-btn>
            </div>
          </v-col>
        </v-row>
        
        <v-divider class="my-4"></v-divider>
        
        <div class="footer-bottom py-4 text-center">
          <p class="text-medium-emphasis mb-0">
            © 2025 Екатерина - кризисный целитель. Все права защищены.
          </p>
        </div>
      </v-container>
    </footer>
  </div>
</template>

<script>
import { ref, onMounted, inject } from 'vue'
import { apiService } from '../services/api.js'
import AOS from 'aos'
import 'aos/dist/aos.css'

export default {
  name: 'Home',
  setup() {
    const products = ref([])
    const quickForm = ref({
      name: '',
      email: '',
      message: ''
    })
    const showSnackbar = inject('showSnackbar', null)

    // Преимущества
    const features = ref([
      {
        icon: 'mdi-shield-lock',
        color: 'primary',
        title: 'Конфиденциальность',
        description: 'Полная конфиденциальность и безопасность ваших личных данных и переживаний'
      },
      {
        icon: 'mdi-heart-pulse',
        color: 'secondary',
        title: 'Эмпатия и забота',
        description: 'Глубокое понимание и поддержка в самые трудные моменты жизни'
      },
      {
        icon: 'mdi-certificate',
        color: 'accent',
        title: 'Проверенные методы',
        description: 'Использую эффективные техники, подтвержденные многолетней практикой'
      }
    ])

    // Отзывы
    const testimonials = ref([
      {
        name: 'Анна С.',
        role: 'Москва',
        text: 'Екатерина помогла мне пережить один из самых тяжелых периодов в жизни. Ее поддержка и профессионализм были бесценны. Благодарю от всего сердца!'
      },
      {
        name: 'Дмитрий К.',
        role: 'Санкт-Петербург',
        text: 'После развода я не знал, как жить дальше. Работа с Екатериной помогла мне найти внутренние силы и начать новую жизнь. Рекомендую!'
      },
      {
        name: 'Мария П.',
        role: 'Казань',
        text: 'Деликатный подход, глубокое понимание и реальная помощь. Екатерина - настоящий профессионал своего дела.'
      }
    ])

    // Шаги процесса
    const steps = ref([
      {
        icon: 'mdi-message-text',
        title: 'Первый контакт',
        description: 'Напишите мне в Telegram и расскажите о вашей ситуации'
      },
      {
        icon: 'mdi-calendar-clock',
        title: 'Согласование',
        description: 'Выберем удобное время и формат работы'
      },
      {
        icon: 'mdi-hand-heart',
        title: 'Работа',
        description: 'Начинаем совместный путь к вашему исцелению'
      },
      {
        icon: 'mdi-emoticon-happy',
        title: 'Результат',
        description: 'Вы обретаете внутреннюю гармонию и силы'
      }
    ])

    const loadProducts = async () => {
      try {
        products.value = await apiService.getPublicProducts()
      } catch (error) {
        console.error('Ошибка загрузки продуктов:', error)
        // Демо продукты
        products.value = [
          {
            id: 1,
            name: 'Базовая консультация',
            description: 'Первичная встреча для знакомства и определения запроса. Длительность 60 минут.',
            price: 3000
          },
          {
            id: 2,
            name: 'Курс "Преодоление кризиса"',
            description: 'Программа из 8 сессий для работы с кризисными состояниями и поиска внутренних ресурсов.',
            price: 20000
          },
          {
            id: 3,
            name: 'Индивидуальная сессия',
            description: 'Глубокая терапевтическая сессия продолжительностью 90 минут.',
            price: 5000
          },
          {
            id: 4,
            name: 'Групповая практика',
            description: 'Участие в групповой целительской практике. Поддержка единомышленников.',
            price: 2000
          }
        ]
      }
    }

    const formatMoney = (amount) => {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
      }).format(amount)
    }

    const getProductIcon = (index) => {
      const icons = ['mdi-chat-outline', 'mdi-book-open-page-variant', 'mdi-account-heart', 'mdi-account-group']
      return icons[index % icons.length]
    }

    const scrollToProducts = () => {
      const element = document.getElementById('products')
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }

    const sendQuickMessage = () => {
      if (!quickForm.value.name || !quickForm.value.email || !quickForm.value.message) {
        if (showSnackbar) {
          showSnackbar('Пожалуйста, заполните все поля', 'error')
        } else {
          alert('Пожалуйста, заполните все поля')
        }
        return
      }

      // Открываем Telegram бот с предзаполненным сообщением
      const message = `Имя: ${quickForm.value.name}\nEmail: ${quickForm.value.email}\nСообщение: ${quickForm.value.message}`
      const encodedMessage = encodeURIComponent(message)
      window.open(`https://t.me/kate202_bot?start=${encodedMessage}`, '_blank')
      
      // Очищаем форму
      quickForm.value = { name: '', email: '', message: '' }
      
      if (showSnackbar) {
        showSnackbar('Сообщение отправлено!', 'success')
      }
    }

    onMounted(() => {
      loadProducts()
      // Инициализация AOS для анимаций с улучшенными настройками
      AOS.init({
        duration: 1000,
        once: true,
        offset: 80,
        easing: 'ease-out-cubic',
        delay: 50,
        anchorPlacement: 'top-bottom',
        disable: false
      })
    })

    return {
      products,
      features,
      testimonials,
      steps,
      quickForm,
      formatMoney,
      getProductIcon,
      scrollToProducts,
      sendQuickMessage
    }
  }
}
</script>

<style scoped>
/* ============================================
   ОБЩИЕ СТИЛИ
   ============================================ */
.home-page {
  overflow-x: hidden;
  margin: 0;
  padding: 0;
}

/* Единые отступы для всех секций */
.section-padding {
  padding: 5rem 0;
}

/* Лейблы секций */
.section-label {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 3px;
  text-transform: uppercase;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* Заголовки секций */
.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.3;
  color: #2d3748;
  letter-spacing: -0.01em;
}

.section-subtitle {
  font-size: 1.25rem;
  color: #718096;
  max-width: 700px;
  margin: 0 auto;
  line-height: 1.7;
  font-weight: 400;
}

.section-text {
  font-size: 1.125rem;
  line-height: 1.8;
  color: #4b5563;
  font-weight: 400;
}

/* ============================================
   HERO СЕКЦИЯ
   ============================================ */
.hero-section {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  overflow: hidden;
}

.hero-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #8B5FBF 0%, #B8A9D8 50%, #D4A5D4 100%);
  z-index: 0;
}

.hero-background::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: 
    radial-gradient(circle at 20% 50%, rgba(255, 255, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(236, 72, 153, 0.1) 0%, transparent 50%);
  animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.hero-content {
  position: relative;
  z-index: 2;
  padding-top: 80px;
  padding-bottom: 80px;
}

.hero-badge {
  animation: float 3s ease-in-out infinite;
}

.hero-badge .v-chip {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.2) !important;
  border: 1px solid rgba(255, 255, 255, 0.3);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.2;
  color: white;
  letter-spacing: -0.01em;
  text-shadow: 0 2px 15px rgba(0, 0, 0, 0.15);
}

.gradient-text {
  background: linear-gradient(135deg, #FFD700 0%, #FFA07A 50%, #FFB6C1 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  animation: gradient-shift 4s ease-in-out infinite;
  background-size: 200% auto;
}

@keyframes gradient-shift {
  0%, 100% { background-position: 0% center; }
  50% { background-position: 100% center; }
}

.hero-subtitle {
  font-size: 1.375rem;
  color: rgba(255, 255, 255, 0.95);
  line-height: 1.8;
  font-weight: 400;
  max-width: 700px;
  margin: 0 auto;
}

.hero-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.telegram-btn {
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
}

.telegram-btn :deep(.v-btn__content) {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}

.telegram-btn :deep(.v-btn__prepend) {
  margin: 0 !important;
}

.catalog-btn {
  background: rgba(255, 255, 255, 0.15) !important;
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.4) !important;
  color: white !important;
  font-weight: 600 !important;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
  display: inline-flex !important;
  align-items: center !important;
  justify-content: center !important;
  text-align: center !important;
  padding: 0 2rem !important;
}

.catalog-btn:hover {
  background: rgba(255, 255, 255, 0.25) !important;
  border-color: rgba(255, 255, 255, 0.6) !important;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(0, 0, 0, 0.25);
}

.stats-row {
  margin-top: 4rem;
}

.stat-item {
  padding: 2rem 1rem;
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1.5rem;
  border: 1px solid rgba(255, 255, 255, 0.2);
  transition: all 0.3s ease;
}

.stat-item:hover {
  transform: translateY(-5px);
  background: rgba(255, 255, 255, 0.15);
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.stat-number {
  font-size: 2.5rem;
  font-weight: 700;
  color: white;
  margin-bottom: 0.5rem;
  line-height: 1.2;
}

.stat-label {
  font-size: 0.95rem;
  color: rgba(255, 255, 255, 0.9);
  font-weight: 400;
  line-height: 1.5;
}

.hero-transition {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 150px;
  background: linear-gradient(to bottom, transparent, rgba(255, 255, 255, 0.1) 30%, rgba(255, 255, 255, 0.5) 60%, #ffffff);
  z-index: 1;
}

@media (max-width: 960px) {
  .hero-transition {
    height: 100px;
  }
}

@media (max-width: 600px) {
  .hero-transition {
    height: 80px;
  }
}

/* ============================================
   О НАС СЕКЦИЯ
   ============================================ */
.about-section {
  background: #ffffff;
}

.about-content {
  padding: 2rem 0;
}

.feature-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1rem;
  color: #374151;
}

.about-image-wrapper {
  position: relative;
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.main-icon {
  opacity: 0.1;
}

.floating-card {
  position: absolute;
  background: white;
  padding: 1.5rem;
  border-radius: 1rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  animation: float 3s ease-in-out infinite;
}

.floating-card-1 {
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.floating-card-2 {
  top: 50%;
  right: 10%;
  animation-delay: 1s;
}

.floating-card-3 {
  bottom: 15%;
  left: 15%;
  animation-delay: 2s;
}

.floating-card-text {
  font-weight: 600;
  font-size: 0.875rem;
  color: #1f2937;
}

/* ============================================
   ПРЕИМУЩЕСТВА
   ============================================ */
.features-section {
  background: #f9fafb;
}

.feature-card {
  border: 1px solid #f0f0f0;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  height: 100%;
  background: white;
  position: relative;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: linear-gradient(to right, #8B5FBF, #D4A5D4);
  transform: scaleX(0);
  transition: transform 0.4s ease;
}

.feature-card::after {
  content: '';
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(139, 95, 191, 0.03), transparent 70%);
  opacity: 0;
  transition: opacity 0.4s ease;
}

.feature-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 40px rgba(139, 95, 191, 0.15) !important;
  border-color: rgba(139, 95, 191, 0.2);
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-card:hover::after {
  opacity: 1;
}

.feature-icon-wrapper {
  width: 90px;
  height: 90px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1), rgba(var(--v-theme-secondary), 0.05));
  border-radius: 1.5rem;
  position: relative;
  transition: all 0.3s ease;
}

.feature-card:hover .feature-icon-wrapper {
  transform: scale(1.1) rotate(5deg);
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.15), rgba(var(--v-theme-secondary), 0.1));
}

/* ============================================
   ПРОДУКТЫ
   ============================================ */
.products-section {
  background: #ffffff;
}

.product-card {
  border: 1px solid #f5f3f7;
  transition: all 0.5s cubic-bezier(0.34, 1.56, 0.64, 1);
  overflow: hidden;
  background: white;
  position: relative;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.04);
}

.product-card::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: 2px;
  background: linear-gradient(135deg, #8B5FBF, #D4A5D4, #FFA07A);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.product-card:hover {
  transform: translateY(-10px) scale(1.01);
  box-shadow: 0 20px 40px rgba(139, 95, 191, 0.2) !important;
  border-color: transparent;
}

.product-card:hover::after {
  opacity: 1;
}

.product-icon-wrapper {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.08), rgba(var(--v-theme-secondary), 0.08));
  padding: 3rem 2rem;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 180px;
  position: relative;
  overflow: hidden;
}

.product-icon-wrapper::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.3) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.product-card:hover .product-icon-wrapper {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.12), rgba(var(--v-theme-secondary), 0.12));
}

.product-description {
  min-height: 60px;
  color: #6b7280;
  line-height: 1.6;
  font-size: 0.95rem;
}

.product-price {
  position: relative;
}

.price-amount {
  font-size: 2.25rem;
  font-weight: 800;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: -0.02em;
}

/* ============================================
   ОТЗЫВЫ
   ============================================ */
.testimonials-section {
  background: #f9fafb;
}

.testimonial-card {
  border: 1px solid #e5e7eb;
  transition: all 0.4s ease;
  background: white;
  position: relative;
  overflow: hidden;
}

.testimonial-card::before {
  content: '"';
  position: absolute;
  top: 10px;
  left: 20px;
  font-size: 80px;
  font-weight: 700;
  color: rgba(var(--v-theme-primary), 0.05);
  font-family: Georgia, serif;
  line-height: 1;
}

.testimonial-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.12) !important;
  border-color: rgba(var(--v-theme-primary), 0.2);
}

.rating {
  display: flex;
  gap: 0.25rem;
}

.testimonial-text {
  font-size: 1rem;
  line-height: 1.7;
  color: #374151;
  font-style: italic;
  font-weight: 400;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.author-avatar {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  box-shadow: 0 4px 12px rgba(var(--v-theme-primary), 0.3);
  position: relative;
}

.author-avatar::before {
  content: '';
  position: absolute;
  inset: -3px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));
  opacity: 0.2;
  filter: blur(8px);
}

.author-name {
  font-weight: 600;
  color: #1f2937;
}

.author-role {
  font-size: 0.875rem;
  color: #6b7280;
}

/* ============================================
   ПРОЦЕСС
   ============================================ */
.process-section {
  background: #ffffff;
}

.process-steps {
  position: relative;
}

.process-step {
  text-align: center;
  position: relative;
  z-index: 2;
}

.step-number {
  width: 50px;
  height: 50px;
  border-radius: 50%;
  background: linear-gradient(135deg, rgb(var(--v-theme-primary)), rgb(var(--v-theme-secondary)));
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 auto 1rem;
  position: relative;
  z-index: 2;
}

.step-icon {
  background: rgba(var(--v-theme-primary), 0.1);
  width: 80px;
  height: 80px;
  border-radius: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1rem;
}

.step-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.75rem;
  line-height: 1.4;
}

.step-description {
  font-size: 0.95rem;
  color: #6b7280;
  line-height: 1.6;
  font-weight: 400;
}

.step-connector {
  position: absolute;
  top: 25px;
  left: 50%;
  width: 100%;
  height: 2px;
  background: linear-gradient(to right, rgb(var(--v-theme-primary)), transparent);
  z-index: 1;
}

/* ============================================
   CTA СЕКЦИЯ
   ============================================ */
.cta-section {
  background: #ffffff;
}

.cta-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2rem !important;
  position: relative;
  overflow: hidden;
}

.cta-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  animation: rotate 20s linear infinite;
}

.cta-subtitle {
  font-size: 1.25rem;
  opacity: 0.95;
}

/* ============================================
   КОНТАКТЫ
   ============================================ */
.contact-section {
  background: #f9fafb;
}

.contact-info {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.contact-item {
  display: flex;
  align-items: flex-start;
  gap: 1rem;
}

.contact-icon {
  width: 50px;
  height: 50px;
  border-radius: 0.75rem;
  background: rgba(var(--v-theme-primary), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.contact-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-bottom: 0.25rem;
  font-weight: 500;
}

.contact-value {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
  line-height: 1.5;
}

.contact-card {
  background: white;
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.contact-card:hover {
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
  border-color: rgba(var(--v-theme-primary), 0.2);
}

/* ============================================
   ФУТЕР
   ============================================ */
.footer-section {
  background: #1f2937;
  color: #e5e7eb;
}

.footer-brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.footer-logo {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
}

.footer-description {
  color: #9ca3af;
  line-height: 1.7;
  font-size: 0.95rem;
  font-weight: 400;
}

.footer-title {
  font-size: 1rem;
  font-weight: 600;
  color: white;
  margin-bottom: 1rem;
}

.footer-links {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.footer-links a {
  color: #9ca3af;
  text-decoration: none;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: white;
}

.footer-social {
  display: flex;
  gap: 0.5rem;
}

.footer-bottom {
  color: #9ca3af;
}

/* ============================================
   АДАПТИВНОСТЬ
   ============================================ */
/* Плавная прокрутка */
html {
  scroll-behavior: smooth;
}

/* Анимация для всех интерактивных элементов */
button, a, .v-btn {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@media (max-width: 960px) {
  .hero-title {
    font-size: 2.5rem;
    line-height: 1.25;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .section-subtitle {
    font-size: 1.125rem;
    line-height: 1.6;
  }
  
  .section-text {
    font-size: 1rem;
    line-height: 1.7;
  }
  
  .about-image-wrapper {
    height: 300px;
    margin-top: 3rem;
  }
  
  .step-connector {
    display: none;
  }
  
  .section-padding {
    padding: 3.5rem 0;
  }
}

@media (max-width: 600px) {
  .hero-title {
    font-size: 1.875rem;
    line-height: 1.3;
  }
  
  .hero-subtitle {
    font-size: 1rem;
    line-height: 1.6;
  }
  
  .section-title {
    font-size: 1.75rem;
    line-height: 1.3;
  }
  
  .section-subtitle {
    font-size: 1rem;
    line-height: 1.6;
  }
  
  .section-text {
    font-size: 0.95rem;
    line-height: 1.6;
  }
  
  .hero-actions {
    flex-direction: column;
    width: 100%;
  }
  
  .hero-actions .v-btn {
    width: 100%;
  }
  
  .stat-item {
    padding: 1.5rem 1rem;
  }
  
  .stat-number {
    font-size: 2rem;
    line-height: 1.2;
  }
  
  .stat-label {
    font-size: 0.875rem;
  }
  
  .step-title {
    font-size: 1rem;
  }
  
  .step-description {
    font-size: 0.875rem;
  }
  
  .section-padding {
    padding: 2.5rem 0;
  }
}
</style> 