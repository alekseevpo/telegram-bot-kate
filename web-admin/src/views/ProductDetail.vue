<template>
  <div class="product-detail-page">
    <!-- Hero секция продукта -->
    <section class="product-hero">
      <v-container>
        <v-row align="center">
          <v-col cols="12" md="6" data-aos="fade-right">
            <div class="product-image-wrapper">
              <div class="product-icon-large">
                <v-icon size="200" :color="product.iconColor || 'primary'">
                  {{ product.icon || 'mdi-package-variant' }}
                </v-icon>
              </div>
              <div class="product-badge">
                <v-chip color="success" variant="flat">
                  <v-icon start>mdi-check-circle</v-icon>
                  Популярный выбор
                </v-chip>
              </div>
            </div>
          </v-col>
          
          <v-col cols="12" md="6" data-aos="fade-left">
            <v-breadcrumbs
              :items="breadcrumbs"
              class="px-0"
            ></v-breadcrumbs>
            
            <h1 class="product-title mb-4">
              {{ product.name }}
            </h1>
            
            <div class="product-rating mb-4">
              <div class="rating-stars">
                <v-icon v-for="i in 5" :key="i" color="warning" size="small">
                  mdi-star
                </v-icon>
              </div>
              <span class="rating-text">(48 отзывов)</span>
            </div>
            
            <p class="product-description-short mb-6">
              {{ product.description }}
            </p>
            
            <div class="product-price-box mb-6">
              <div class="price-current">{{ formatMoney(product.price) }}</div>
              <div class="price-label">Единоразовый платеж</div>
            </div>
            
            <div class="product-actions mb-6">
              <v-btn
                color="primary"
                size="x-large"
                variant="flat"
                block
                href="https://t.me/kate202_bot"
                target="_blank"
                prepend-icon="mdi-cart"
                class="mb-3"
              >
                Заказать сейчас
              </v-btn>
              
              <v-btn
                color="primary"
                size="large"
                variant="outlined"
                block
                @click="scrollToDetails"
                prepend-icon="mdi-information"
              >
                Узнать подробнее
              </v-btn>
            </div>
            
            <div class="product-features">
              <div class="feature-item-inline">
                <v-icon color="success" size="small">mdi-check</v-icon>
                <span>Гарантия качества</span>
              </div>
              <div class="feature-item-inline">
                <v-icon color="success" size="small">mdi-check</v-icon>
                <span>Поддержка 24/7</span>
              </div>
              <div class="feature-item-inline">
                <v-icon color="success" size="small">mdi-check</v-icon>
                <span>Быстрое получение</span>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Что включено -->
    <section class="product-includes py-16" id="details">
      <v-container>
        <div class="text-center mb-12" data-aos="fade-up">
          <h2 class="section-title mb-4">Что входит в продукт</h2>
          <p class="section-subtitle">
            Полный набор инструментов и материалов для достижения результата
          </p>
        </div>
        
        <v-row>
          <v-col 
            v-for="(item, index) in includes" 
            :key="index"
            cols="12" 
            md="6"
            data-aos="fade-up"
            :data-aos-delay="index * 100"
          >
            <v-card class="include-card h-100">
              <v-card-text class="pa-6">
                <div class="d-flex align-start">
                  <div class="include-icon mr-4">
                    <v-icon :color="item.color" size="30">{{ item.icon }}</v-icon>
                  </div>
                  <div>
                    <h3 class="include-title mb-2">{{ item.title }}</h3>
                    <p class="include-description">{{ item.description }}</p>
                  </div>
                </div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- Преимущества -->
    <section class="product-benefits py-16">
      <v-container>
        <div class="text-center mb-12" data-aos="fade-up">
          <h2 class="section-title mb-4">Преимущества этого продукта</h2>
          <p class="section-subtitle">
            Почему стоит выбрать именно этот курс
          </p>
        </div>
        
        <v-row align="center">
          <v-col cols="12" md="6" data-aos="fade-right">
            <div class="benefits-image">
              <v-icon size="300" color="primary" style="opacity: 0.1;">
                mdi-trophy-award
              </v-icon>
            </div>
          </v-col>
          
          <v-col cols="12" md="6" data-aos="fade-left">
            <div class="benefits-list">
              <div 
                v-for="(benefit, index) in benefits" 
                :key="index"
                class="benefit-item"
              >
                <div class="benefit-number">{{ index + 1 }}</div>
                <div>
                  <h4 class="benefit-title">{{ benefit.title }}</h4>
                  <p class="benefit-text">{{ benefit.text }}</p>
                </div>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- FAQ -->
    <section class="product-faq py-16">
      <v-container>
        <div class="text-center mb-12" data-aos="fade-up">
          <h2 class="section-title mb-4">Частые вопросы</h2>
          <p class="section-subtitle">
            Ответы на популярные вопросы о продукте
          </p>
        </div>
        
        <v-row justify="center">
          <v-col cols="12" md="8" data-aos="fade-up">
            <v-expansion-panels variant="accordion">
              <v-expansion-panel
                v-for="(faq, index) in faqs"
                :key="index"
              >
                <v-expansion-panel-title class="text-h6 font-weight-medium">
                  {{ faq.question }}
                </v-expansion-panel-title>
                <v-expansion-panel-text>
                  {{ faq.answer }}
                </v-expansion-panel-text>
              </v-expansion-panel>
            </v-expansion-panels>
          </v-col>
        </v-row>
      </v-container>
    </section>

    <!-- CTA -->
    <section class="product-cta py-16">
      <v-container>
        <v-card class="cta-card" elevation="0" data-aos="zoom-in">
          <v-card-text class="pa-12 text-center">
            <h2 class="section-title text-white mb-4">
              Готовы начать путь к исцелению?
            </h2>
            <p class="cta-subtitle text-white mb-8">
              Присоединяйтесь к {{ product.students || '500+' }} людям, обретшим гармонию
            </p>
            <div class="d-flex justify-center align-center gap-4 flex-wrap">
              <v-btn
                color="white"
                size="x-large"
                variant="flat"
                href="https://t.me/kate202_bot"
                target="_blank"
                prepend-icon="mdi-cart"
              >
                Заказать за {{ formatMoney(product.price) }}
              </v-btn>
              <v-btn
                color="white"
                size="x-large"
                variant="outlined"
                @click="$router.push('/')"
                prepend-icon="mdi-arrow-left"
              >
                Вернуться к каталогу
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-container>
    </section>
  </div>
</template>

<script>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AOS from 'aos'
import 'aos/dist/aos.css'

export default {
  name: 'ProductDetail',
  setup() {
    const route = useRoute()
    const router = useRouter()
    
    // Демо данные продукта (в реальности загружаем из API)
    const product = ref({
      id: route.params.id || 1,
      name: 'Базовая консультация',
      description: 'Первичная встреча для знакомства и определения запроса. Вместе мы найдем путь к вашему исцелению.',
      price: 3000,
      icon: 'mdi-chat-outline',
      iconColor: 'primary',
      students: '300+'
    })

    const breadcrumbs = computed(() => [
      { title: 'Главная', to: '/', disabled: false },
      { title: 'Каталог', to: '/#products', disabled: false },
      { title: product.value.name, disabled: true }
    ])

    const includes = ref([
      {
        icon: 'mdi-video-box',
        color: 'primary',
        title: 'Онлайн сессия 60 минут',
        description: 'Полноценная встреча в удобном для вас формате через видеосвязь'
      },
      {
        icon: 'mdi-shield-lock',
        color: 'secondary',
        title: 'Конфиденциальность',
        description: 'Полная конфиденциальность наших встреч гарантирована'
      },
      {
        icon: 'mdi-heart-pulse',
        color: 'accent',
        title: 'Индивидуальный подход',
        description: 'Работа с вашей уникальной ситуацией и запросом'
      },
      {
        icon: 'mdi-file-document-edit',
        color: 'success',
        title: 'Практические инструменты',
        description: 'Получите техники и упражнения для самостоятельной работы'
      },
      {
        icon: 'mdi-message-text',
        color: 'info',
        title: 'Поддержка между сессиями',
        description: 'Возможность написать в случае острой необходимости'
      },
      {
        icon: 'mdi-calendar-check',
        color: 'warning',
        title: 'Гибкое расписание',
        description: 'Подберем удобное для вас время встречи'
      }
    ])

    const benefits = ref([
      {
        title: 'Многолетний опыт',
        text: 'Более 10 лет опыта работы с людьми в кризисных состояниях'
      },
      {
        title: 'Проверенные методики',
        text: 'Использую эффективные техники, которые действительно работают'
      },
      {
        title: 'Безопасное пространство',
        text: 'Создаю атмосферу принятия, где вы можете быть собой'
      },
      {
        title: 'Реальные результаты',
        text: 'Сотни людей уже обрели внутреннюю гармонию благодаря нашей работе'
      }
    ])

    const faqs = ref([
      {
        question: 'Как проходят консультации?',
        answer: 'Консультации проходят онлайн через защищенную видеосвязь. Вы можете находиться в любом удобном для вас месте.'
      },
      {
        question: 'Нужна ли подготовка к первой встрече?',
        answer: 'Нет, специальной подготовки не требуется. Просто будьте готовы открыто поговорить о том, что вас беспокоит.'
      },
      {
        question: 'Гарантируется ли конфиденциальность?',
        answer: 'Абсолютно. Все, что вы расскажете на сессиях, останется между нами. Это основа нашей работы.'
      },
      {
        question: 'Что если мне не подойдет?',
        answer: 'Если после первой консультации вы поймете, что вам не подходит, мы вернем вам оплату.'
      },
      {
        question: 'Как быстро будет результат?',
        answer: 'Каждый случай индивидуален. Некоторые чувствуют облегчение уже после первой встречи, для других процесс требует времени.'
      }
    ])

    const formatMoney = (amount) => {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB',
        minimumFractionDigits: 0
      }).format(amount)
    }

    const scrollToDetails = () => {
      const element = document.getElementById('details')
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' })
      }
    }

    onMounted(() => {
      AOS.init({
        duration: 800,
        once: true
      })
    })

    return {
      product,
      breadcrumbs,
      includes,
      benefits,
      faqs,
      formatMoney,
      scrollToDetails
    }
  }
}
</script>

<style scoped>
/* Hero секция */
.product-hero {
  padding: 6rem 0 4rem;
  background: linear-gradient(to bottom, #f9fafb, #ffffff);
}

.product-image-wrapper {
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.product-icon-large {
  background: linear-gradient(135deg, rgba(var(--v-theme-primary), 0.1), rgba(var(--v-theme-secondary), 0.1));
  border-radius: 2rem;
  padding: 3rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.product-badge {
  position: absolute;
  top: 20px;
  right: 20px;
}

.product-title {
  font-size: 3rem;
  font-weight: 800;
  line-height: 1.2;
  color: #1f2937;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.rating-stars {
  display: flex;
  gap: 0.25rem;
}

.rating-text {
  color: #6b7280;
}

.product-description-short {
  font-size: 1.125rem;
  line-height: 1.75;
  color: #4b5563;
}

.product-price-box {
  background: linear-gradient(135deg, #f9fafb, #ffffff);
  border: 2px solid #e5e7eb;
  border-radius: 1rem;
  padding: 1.5rem;
}

.price-current {
  font-size: 2.5rem;
  font-weight: 700;
  color: rgb(var(--v-theme-primary));
}

.price-label {
  color: #6b7280;
  font-size: 0.875rem;
}

.product-features {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.feature-item-inline {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: #374151;
  font-weight: 500;
}

/* Что включено */
.product-includes {
  background: #ffffff;
}

.include-card {
  border: 1px solid #e5e7eb;
  transition: all 0.3s ease;
}

.include-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1) !important;
  border-color: rgb(var(--v-theme-primary));
}

.include-icon {
  width: 60px;
  height: 60px;
  border-radius: 0.75rem;
  background: rgba(var(--v-theme-primary), 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.include-title {
  font-size: 1.125rem;
  font-weight: 600;
  color: #1f2937;
}

.include-description {
  font-size: 0.875rem;
  color: #6b7280;
  line-height: 1.5;
  margin-bottom: 0;
}

/* Преимущества */
.product-benefits {
  background: #f9fafb;
}

.benefits-image {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 400px;
}

.benefits-list {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.benefit-item {
  display: flex;
  gap: 1.5rem;
}

.benefit-number {
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
  flex-shrink: 0;
}

.benefit-title {
  font-size: 1.25rem;
  font-weight: 600;
  color: #1f2937;
  margin-bottom: 0.5rem;
}

.benefit-text {
  font-size: 1rem;
  color: #6b7280;
  line-height: 1.75;
  margin-bottom: 0;
}

/* FAQ */
.product-faq {
  background: #ffffff;
}

/* CTA */
.product-cta {
  background: #f9fafb;
}

.cta-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2rem !important;
}

.cta-subtitle {
  font-size: 1.25rem;
  opacity: 0.95;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  color: #1f2937;
}

.section-subtitle {
  font-size: 1.125rem;
  color: #6b7280;
  max-width: 600px;
  margin: 0 auto;
}

/* Адаптивность */
@media (max-width: 960px) {
  .product-title {
    font-size: 2rem;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .product-hero {
    padding: 4rem 0 2rem;
  }
}
</style>

