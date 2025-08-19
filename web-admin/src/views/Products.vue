<template>
  <div>
    <v-row class="mb-6">
      <v-col>
        <h1 class="text-h4 font-weight-bold mb-2">📦 Продукты</h1>
        <p class="text-subtitle-1 text-medium-emphasis">Управление каталогом продуктов</p>
      </v-col>
      <v-col cols="auto">
        <v-btn color="primary" @click="createProduct" prepend-icon="mdi-plus">
          Добавить продукт
        </v-btn>
      </v-col>
    </v-row>

    <!-- Таблица продуктов -->
    <v-card>
      <v-card-title>
        <v-icon class="mr-2">mdi-package-variant</v-icon>
        Список продуктов ({{ products.length }})
      </v-card-title>
      
      <v-data-table
        :headers="headers"
        :items="products"
        :loading="loading"
        class="elevation-1"
      >
        <template v-slot:item.price="{ item }">
          {{ formatMoney(item.price) }}
        </template>
        
        <template v-slot:item.description="{ item }">
          <div class="text-truncate" style="max-width: 200px;">
            {{ item.description }}
          </div>
        </template>
        
        <template v-slot:item.actions="{ item }">
          <v-btn 
            icon="mdi-pencil" 
            size="small" 
            variant="text"
            @click="editProduct(item)"
          ></v-btn>
          <v-btn 
            icon="mdi-delete" 
            size="small" 
            variant="text"
            color="error"
            @click="deleteProduct(item)"
          ></v-btn>
        </template>
      </v-data-table>
    </v-card>

    <!-- Диалог редактирования продукта -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <v-icon class="mr-2">{{ isEditing ? 'mdi-pencil' : 'mdi-plus' }}</v-icon>
          {{ isEditing ? 'Редактировать продукт' : 'Добавить продукт' }}
        </v-card-title>
        
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="editedProduct.name"
              label="Название продукта"
              variant="outlined"
              required
              class="mb-4"
            ></v-text-field>
            
            <v-text-field
              v-model.number="editedProduct.price"
              label="Цена (руб.)"
              type="number"
              variant="outlined"
              required
              class="mb-4"
            ></v-text-field>
            
            <v-textarea
              v-model="editedProduct.description"
              label="Описание"
              variant="outlined"
              rows="4"
            ></v-textarea>
          </v-form>
        </v-card-text>
        
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn variant="text" @click="dialog = false">Отмена</v-btn>
          <v-btn color="primary" @click="saveProduct" :loading="saving">
            {{ isEditing ? 'Сохранить' : 'Создать' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { ref, computed, onMounted, inject } from 'vue'
import { apiService } from '../services/api.js'

export default {
  name: 'Products',
  setup() {
    const products = ref([])
    const loading = ref(false)
    const saving = ref(false)
    const dialog = ref(false)
    const editedProduct = ref({})
    const editedIndex = ref(-1)
    const showSnackbar = inject('showSnackbar')

    const headers = [
      { title: 'ID', key: 'id', align: 'start' },
      { title: 'Название', key: 'name' },
      { title: 'Цена', key: 'price' },
      { title: 'Описание', key: 'description' },
      { title: 'Действия', key: 'actions', sortable: false }
    ]

    const isEditing = computed(() => editedIndex.value > -1)

    const loadProducts = async () => {
      loading.value = true
      try {
        products.value = await apiService.getProducts()
      } catch (error) {
        console.error('Ошибка загрузки продуктов:', error)
        showSnackbar('Ошибка загрузки продуктов', 'error')
      } finally {
        loading.value = false
      }
    }

    const createProduct = () => {
      editedProduct.value = { name: '', price: 0, description: '' }
      editedIndex.value = -1
      dialog.value = true
    }

    const editProduct = (product) => {
      editedProduct.value = { ...product }
      editedIndex.value = products.value.indexOf(product)
      dialog.value = true
    }

    const deleteProduct = async (product) => {
      if (confirm('Вы уверены, что хотите удалить этот продукт?')) {
        try {
          await apiService.deleteProduct(product.id)
          showSnackbar('Продукт успешно удален', 'success')
          await loadProducts()
        } catch (error) {
          console.error('Ошибка удаления продукта:', error)
          showSnackbar('Ошибка удаления продукта', 'error')
        }
      }
    }

    const saveProduct = async () => {
      saving.value = true
      try {
        if (isEditing.value) {
          await apiService.updateProduct(editedProduct.value.id, editedProduct.value)
          showSnackbar('Продукт успешно обновлен', 'success')
        } else {
          await apiService.createProduct(editedProduct.value)
          showSnackbar('Продукт успешно создан', 'success')
        }
        
        dialog.value = false
        await loadProducts()
      } catch (error) {
        console.error('Ошибка сохранения продукта:', error)
        showSnackbar('Ошибка сохранения продукта', 'error')
      } finally {
        saving.value = false
      }
    }

    const formatMoney = (amount) => {
      return new Intl.NumberFormat('ru-RU', {
        style: 'currency',
        currency: 'RUB'
      }).format(amount)
    }

    onMounted(() => {
      loadProducts()
    })

    return {
      products,
      loading,
      saving,
      dialog,
      editedProduct,
      isEditing,
      headers,
      loadProducts,
      createProduct,
      editProduct,
      deleteProduct,
      saveProduct,
      formatMoney
    }
  }
}
</script> 