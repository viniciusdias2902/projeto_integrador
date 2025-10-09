<script setup>
import { ref, onMounted } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import { useDelayedLoading } from '@/useDelayedLoading'
import DefaultLayout from '@/templates/DefaultLayout.vue'

const POLLS_URL = `${import.meta.env.VITE_APP_API_URL}polls/`

const polls = ref([])
const errorMessage = ref('')
const { isLoading, executeWithLoading } = useDelayedLoading(500)
const isInitialLoad = ref(true)

const diasSemana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

function getDiaSemana(dateString) {
  const date = new Date(`${dateString}T00:00:00`)
  return diasSemana[date.getDay()]
}

function formatDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  return `${day}/${month}`
}

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
}

async function getPolls(withDelay = false) {
  try {
    await executeWithLoading(() => fetchPolls(), withDelay)
  } catch (error) {
    console.error('Error fetching polls:', error)
    errorMessage.value = error.message || 'Erro ao carregar enquetes. Tente novamente.'
  } finally {
    isInitialLoad.value = false
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
        <h1 class="text-4xl font-bold mb-2">Enquetes de Transporte</h1>
        <p class="text-base-content/70">
          Hoje é {{ diasSemana[new Date().getDay()] }} - Vote nas enquetes da semana
        </p>
      </div>

      <!-- Loading state -->
      <div v-if="showLoadingSkeleton" class="flex flex-wrap gap-4 items-center justify-center">
        <div v-for="n in 5" :key="n" class="w-64 h-96">
          <div class="skeleton h-full w-full rounded-box"></div>
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

      <!-- Empty state -->
      <div v-else-if="!polls.length" class="flex justify-center">
        <div class="alert alert-info max-w-md">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" class="stroke-current shrink-0 w-6 h-6">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
          <div>
            <h3 class="font-bold">Nenhuma enquete disponível</h3>
            <div class="text-sm">Não há enquetes ativas no momento.</div>
          </div>
        </div>
      </div>

      <!-- Polls grid -->
      <div 
        v-else 
        class="flex flex-wrap gap-4 items-start justify-center max-w-7xl mx-auto"
      >
        <PollComponent
          v-for="poll in polls"
          :key="poll.id"
          :name="poll.id"
          :day="`${getDiaSemana(poll.date)} - ${formatDate(poll.date)}`"
          :date="poll.date"
        />
      </div>

      <!-- Refresh button -->
      <div v-if="polls.length > 0" class="mt-8 text-center">
        <button 
          class="btn btn-outline btn-sm"
          @click="getPolls(true)"
          :disabled="isLoading"
        >
          <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
          <svg v-else xmlns="http://www.w3.org/2000/svg" class="h-4 w-4 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
          </svg>
          {{ isLoading ? 'Atualizando...' : 'Atualizar enquetes' }}
        </button>
      </div>
    </div>
  </DefaultLayout>
</template>