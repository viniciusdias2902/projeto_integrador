<script setup>
import { ref, onMounted } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import PaymentStatusChart from '@/components/PaymentStatusChart.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const students = ref([])
const isLoading = ref(false)
const errorMessage = ref('')

async function fetchStudents() {
  errorMessage.value = ''
  isLoading.value = true

  const isValid = await verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    isLoading.value = false
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}students/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      throw new Error('Erro ao carregar estudantes')
    }

    const data = await response.json()
    students.value = data
  } catch (error) {
    console.error('Error fetching students:', error)
    errorMessage.value = 'Erro ao carregar estudantes. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchStudents()
})
</script>

<template>
  <DefaultLayout>
    <div class="container mx-auto px-4 py-8">
      <div class="mb-8">
        <h1 class="text-4xl font-bold mb-2">Dashboard Administrativo</h1>
        <p class="text-base-content/70">Visualize estatísticas e métricas dos estudantes</p>
      </div>

      <div v-if="errorMessage" class="alert alert-error mb-4">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="stroke-current shrink-0 h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>{{ errorMessage }}</span>
      </div>

      <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
        <span class="loading loading-spinner loading-lg"></span>
      </div>

      <div v-else class="grid grid-cols-1 gap-6">
        <PaymentStatusChart :students="students" />
      </div>
    </div>
  </DefaultLayout>
</template>
