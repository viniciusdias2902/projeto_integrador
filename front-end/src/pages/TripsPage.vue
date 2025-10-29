<script setup>
import { ref, onMounted, computed, watch } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import { usePolling } from '@/composables/usePolling'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import TripController from '@/components/TripController.vue'
import TripSelector from '@/components/TripSelector.vue'
import TripMessages from '@/components/TripMessages.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const polls = ref([])
const selectedPollId = ref(null)
const selectedTripType = ref('outbound')
const activeTrip = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const hasActiveTrip = computed(() => activeTrip.value !== null)

const selectedPoll = computed(() => {
  if (!selectedPollId.value) return null
  return polls.value.find((p) => p.id === selectedPollId.value)
})

// ✅ REMOVIDO: Polling desnecessário em TripsPage
// O polling já é feito em TripController, não precisa duplicar aqui

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

async function initializeTrip() {
  if (!selectedPollId.value) {
    errorMessage.value = 'Selecione uma enquete primeiro'
    return
  }

  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    await checkExistingTrip()

    if (!activeTrip.value) {
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

function handleTripCompleted() {
  activeTrip.value = null
  successMessage.value = 'Viagem concluída com sucesso!'

  setTimeout(() => {
    successMessage.value = ''
  }, 5000)
}

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
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">Gerenciamento de Viagens</h1>
        <p class="text-base-content/70">Controle as viagens de transporte</p>
      </div>

      <TripMessages :error-message="errorMessage" :success-message="successMessage" />

      <div
        v-if="isLoading && !hasActiveTrip"
        class="flex justify-center items-center min-h-[400px]"
      >
        <div class="text-center">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4 text-base-content/70">Carregando...</p>
        </div>
      </div>

      <!-- ✅ Usar key para evitar re-render desnecessário -->
      <TripSelector
        v-else-if="!hasActiveTrip"
        :key="`selector-${selectedPollId}-${selectedTripType}`"
        :polls="polls"
        :selected-poll-id="selectedPollId"
        :selected-trip-type="selectedTripType"
        :selected-poll="selectedPoll"
        :is-loading="isLoading"
        @update:selected-poll-id="
          (value) => {
            selectedPollId = value
            handleSelectionChange()
          }
        "
        @update:selected-trip-type="
          (value) => {
            selectedTripType = value
            handleSelectionChange()
          }
        "
        @initialize-trip="initializeTrip"
      />

      <!-- ✅ TripController gerencia seu próprio polling internamente -->
      <TripController
        v-if="hasActiveTrip"
        :key="`controller-${activeTrip.id}`"
        :trip="activeTrip"
        @trip-updated="activeTrip = $event"
        @trip-completed="handleTripCompleted"
      />
    </div>
  </DefaultLayout>
</template>
