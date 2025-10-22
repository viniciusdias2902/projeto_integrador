<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import TripController from '@/components/TripController.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const polls = ref([])
const selectedPollId = ref(null)
const selectedTripType = ref('outbound')
const activeTrip = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const diasSemana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

const tripTypeOptions = [
  { value: 'outbound', label: 'Ida' },
  { value: 'return', label: 'Volta' },
]

// Computed para verificar se há uma viagem ativa
const hasActiveTrip = computed(() => activeTrip.value !== null)

// Computed para obter informações da enquete selecionada
const selectedPoll = computed(() => {
  if (!selectedPollId.value) return null
  return polls.value.find((p) => p.id === selectedPollId.value)
})

// Formatar data da enquete
function formatPollDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const weekday = diasSemana[date.getDay()]
  return `${weekday}, ${day}/${month}`
}

// Buscar enquetes disponíveis
async function fetchPolls() {
  errorMessage.value = ''
  isLoading.value = true

  const isValid = verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Sessão expirada. Faça login novamente.'
    isLoading.value = false
    return
  }

  try {
    const response = await fetch(`${API_BASE_URL}polls/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      throw new Error('Erro ao carregar enquetes')
    }

    const data = await response.json()
    polls.value = data

    // Selecionar automaticamente a enquete de hoje se existir
    const today = new Date().toISOString().split('T')[0]
    const todayPoll = data.find((poll) => poll.date === today)
    if (todayPoll) {
      selectedPollId.value = todayPoll.id
    }
  } catch (error) {
    console.error('Error fetching polls:', error)
    errorMessage.value = 'Erro ao carregar enquetes. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

// Verificar se já existe uma viagem para a enquete e tipo selecionados
async function checkExistingTrip() {
  if (!selectedPollId.value) return

  try {
    const response = await fetch(
      `${API_BASE_URL}trips/?poll_id=${selectedPollId.value}&trip_type=${selectedTripType.value}`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      },
    )

    if (!response.ok) {
      throw new Error('Erro ao verificar viagem existente')
    }

    const trips = await response.json()
    if (trips.length > 0) {
      activeTrip.value = trips[0]
    } else {
      activeTrip.value = null
    }
  } catch (error) {
    console.error('Error checking existing trip:', error)
  }
}

// Criar ou carregar viagem
async function initializeTrip() {
  if (!selectedPollId.value) {
    errorMessage.value = 'Selecione uma enquete primeiro'
    return
  }

  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    // Verificar se já existe uma viagem
    await checkExistingTrip()

    if (!activeTrip.value) {
      // Criar nova viagem
      const response = await fetch(`${API_BASE_URL}trips/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
        body: JSON.stringify({
          poll: selectedPollId.value,
          trip_type: selectedTripType.value,
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Erro ao criar viagem')
      }

      activeTrip.value = await response.json()
      successMessage.value = 'Viagem criada com sucesso!'
    } else {
      successMessage.value = 'Viagem carregada!'
    }
  } catch (error) {
    console.error('Error initializing trip:', error)
    errorMessage.value = error.message || 'Erro ao inicializar viagem'
  } finally {
    isLoading.value = false
  }
}

// Callback quando a viagem é completada
function handleTripCompleted() {
  activeTrip.value = null
  successMessage.value = 'Viagem concluída com sucesso!'

  setTimeout(() => {
    successMessage.value = ''
  }, 5000)
}

// Atualizar viagem ativa quando poll ou tipo mudar
async function handleSelectionChange() {
  activeTrip.value = null
  if (selectedPollId.value) {
    await checkExistingTrip()
  }
}

onMounted(() => {
  fetchPolls()
})
</script>

<template>
  <DefaultLayout>
    <div class="container mx-auto px-4 py-8 max-w-4xl">
      <!-- Cabeçalho -->
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">Gerenciamento de Viagens</h1>
        <p class="text-base-content/70">Controle as viagens de transporte</p>
      </div>

      <!-- Mensagens de feedback -->
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

      <div v-if="successMessage" class="alert alert-success mb-4">
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
            d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <span>{{ successMessage }}</span>
      </div>

      <!-- Loading state -->
      <div
        v-if="isLoading && !hasActiveTrip"
        class="flex justify-center items-center min-h-[400px]"
      >
        <div class="text-center">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4 text-base-content/70">Carregando...</p>
        </div>
      </div>

      <!-- Seleção de enquete e tipo (apenas se não houver viagem ativa) -->
      <div v-else-if="!hasActiveTrip" class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title">Selecione a Viagem</h2>

          <!-- Seletor de enquete -->
          <div class="form-control w-full">
            <label class="label">
              <span class="label-text">Enquete (Dia)</span>
            </label>
            <select
              v-model="selectedPollId"
              class="select select-bordered w-full"
              @change="handleSelectionChange"
              :disabled="polls.length === 0"
            >
              <option :value="null" disabled>Selecione uma enquete</option>
              <option v-for="poll in polls" :key="poll.id" :value="poll.id">
                {{ formatPollDate(poll.date) }}
              </option>
            </select>
          </div>

          <!-- Seletor de tipo de viagem -->
          <div class="form-control w-full">
            <label class="label">
              <span class="label-text">Tipo de Viagem</span>
            </label>
            <select
              v-model="selectedTripType"
              class="select select-bordered w-full"
              @change="handleSelectionChange"
            >
              <option v-for="option in tripTypeOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>

          <!-- Informações da seleção -->
          <div v-if="selectedPoll" class="alert alert-info mt-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
              class="stroke-current shrink-0 w-6 h-6"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              ></path>
            </svg>
            <div>
              <p class="font-bold">{{ formatPollDate(selectedPoll.date) }}</p>
              <p class="text-sm">{{ selectedTripType === 'outbound' ? 'Ida' : 'Volta' }}</p>
            </div>
          </div>

          <!-- Botão de iniciar -->
          <div class="card-actions justify-end mt-4">
            <button
              class="btn btn-primary btn-block"
              @click="initializeTrip"
              :disabled="!selectedPollId || isLoading"
            >
              <svg
                v-if="isLoading"
                class="animate-spin h-5 w-5 mr-2"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  class="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  stroke-width="4"
                ></circle>
                <path
                  class="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
              {{ isLoading ? 'Carregando...' : 'Carregar Viagem' }}
            </button>
          </div>
        </div>
      </div>

      <!-- Controlador de viagem ativa -->
      <TripController
        v-if="hasActiveTrip"
        :trip="activeTrip"
        @trip-updated="activeTrip = $event"
        @trip-completed="handleTripCompleted"
      />
    </div>
  </DefaultLayout>
</template>
