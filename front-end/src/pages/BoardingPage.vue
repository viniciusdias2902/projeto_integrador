<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import { useDelayedLoading } from '@/useDelayedLoading'
const POLLS_URL = `${import.meta.env.VITE_APP_API_URL}polls/`

const polls = ref([])
const errorMessage = ref('')
const { isLoading, executeWithLoading } = useDelayedLoading(500)

const diasSemana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

// Computed para pegar a enquete de hoje
const todaysPoll = computed(() => {
  const today = new Date().toISOString().split('T')[0]
  return polls.value.find(poll => poll.date === today)
})

// Computed para o dia da semana de hoje
const todayWeekday = computed(() => {
  return diasSemana[new Date().getDay()]
})

async function fetchPolls() {
  errorMessage.value = ''
  
  const isValid = verifyAndRefreshToken()
  
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    throw new Error('Sessão expirada')
  }

  const response = await fetch(POLLS_URL, {
    headers: { 
      Authorization: `Bearer ${localStorage.getItem('access')}` 
    },
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.detail || 'Erro ao carregar enquetes')
  }

  const data = await response.json()
  polls.value = data
  
  console.log('Polls loaded:', polls.value)
  console.log('Today\'s poll:', todaysPoll.value)
}

async function getPolls(withDelay = false) {
  try {
    await executeWithLoading(() => fetchPolls(), withDelay)
  } catch (error) {
    console.error('Error fetching polls:', error)
    errorMessage.value = error.message || 'Erro ao carregar dados. Tente novamente.'
  }
}

onMounted(() => {
  getPolls(false) // Sem delay no mount inicial
})
</script>

<template>
  <DefaultLayout>
    <div class="container mx-auto px-4 py-8">
      <!-- Cabeçalho -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">Lista de Embarque</h1>
        <p class="text-base-content/70">
          {{ todayWeekday }} - {{ new Date().toLocaleDateString('pt-BR') }}
        </p>
      </div>

      <!-- Loading state -->
      <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
        <div class="text-center">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4 text-base-content/70">Buscando enquete do dia...</p>
        </div>
      </div>

      <!-- Error state -->
      <div v-else-if="errorMessage" class="flex justify-center">
        <div class="alert alert-error max-w-md">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <div>
            <h3 class="font-bold">Erro ao carregar</h3>
            <div class="text-sm">{{ errorMessage }}</div>
          </div>
          <button class="btn btn-sm btn-ghost" @click="getPolls(false)">Tentar novamente</button>
        </div>
      </div>

      <!-- No poll for today -->
      <div v-else-if="!todaysPoll" class="flex justify-center">
        <div class="alert alert-warning max-w-md">
          <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 w-6 h-6" fill="none" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
          </svg>
          <div>
            <h3 class="font-bold">Nenhuma enquete para hoje</h3>
            <div class="text-sm">Não há enquete cadastrada para {{ todayWeekday }}.</div>
          </div>
        </div>
      </div>

      <!-- Boarding lists -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <BoardingComponent 
          boarding-type="Ida" 
          :poll-id="todaysPoll.id"
          :poll-date="todaysPoll.date"
        />
        <BoardingComponent 
          boarding-type="Volta" 
          :poll-id="todaysPoll.id"
          :poll-date="todaysPoll.date"
        />
      </div>

      <!-- Refresh button -->
      <div v-if="todaysPoll" class="mt-8 text-center">
        <button 
          class="btn btn-outline btn-sm"
          @click="getPolls(true)"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ isLoading ? 'Atualizando...' : 'Atualizar listas' }}
        </button>
      </div>
    </div>
  </DefaultLayout>
</template>