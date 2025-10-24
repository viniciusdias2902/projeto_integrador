<script setup>
import { ref, onMounted, computed, watch, onUnmounted } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import { usePolling } from '@/composables/usePolling'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import TripViewCard from '@/components/TripViewCard.vue'
import TripMessages from '@/components/TripMessages.vue'
import CurrentBoardingPoint from '@/components/CurrentBoardingPoint.vue'
import AllBoardingPoints from '@/components/AllBoardingPoints.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const todayPoll = ref(null)
const outboundTrip = ref(null)
const returnTrip = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const lastUpdate = ref(new Date())

const hasActiveTrip = computed(() => {
  return (
    (outboundTrip.value && outboundTrip.value.status === 'in_progress') ||
    (returnTrip.value && returnTrip.value.status === 'in_progress')
  )
})

const { startPolling, stopPolling } = usePolling(async () => {
  await verifyAndRefreshToken()
  await refreshTripStatus()
}, 5000)

async function refreshTripStatus() {
  if (!todayPoll.value) return

  try {
    // Atualizar viagem de ida
    if (outboundTrip.value) {
      const outResponse = await fetch(`${API_BASE_URL}trips/${outboundTrip.value.id}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      })

      if (outResponse.ok) {
        const data = await outResponse.json()
        outboundTrip.value = data
        lastUpdate.value = new Date()
      }
    }

    // Atualizar viagem de volta
    if (returnTrip.value) {
      const retResponse = await fetch(`${API_BASE_URL}trips/${returnTrip.value.id}/`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      })

      if (retResponse.ok) {
        const data = await retResponse.json()
        returnTrip.value = data
        lastUpdate.value = new Date()
      }
    }

    // Se não há viagem de volta mas a ida foi concluída, verificar se foi criada
    if (outboundTrip.value?.status === 'completed' && !returnTrip.value) {
      await loadTrips(false) // Recarregar sem loading
    }
  } catch (error) {
    console.error('Error refreshing trip status:', error)
  }
}

async function fetchTodayPoll() {
  errorMessage.value = ''
  isLoading.value = true

  const isValid = await verifyAndRefreshToken()
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

    const polls = await response.json()
    const today = new Date().toISOString().split('T')[0]
    todayPoll.value = polls.find((poll) => poll.date === today)

    if (!todayPoll.value) {
      errorMessage.value = 'Não há enquete para hoje'
      isLoading.value = false
      return
    }

    await loadTrips(true)
  } catch (error) {
    console.error('Error fetching polls:', error)
    errorMessage.value = 'Erro ao carregar dados. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

async function loadTrips(showLoading = true) {
  if (!todayPoll.value) return

  if (showLoading) {
    isLoading.value = true
  }

  try {
    // Buscar viagem de ida
    const outboundResponse = await fetch(
      `${API_BASE_URL}trips/?poll_id=${todayPoll.value.id}&trip_type=outbound`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      },
    )

    if (outboundResponse.ok) {
      const outboundTrips = await outboundResponse.json()
      if (outboundTrips.length > 0) {
        const tripId = outboundTrips[0].id
        const detailsResponse = await fetch(`${API_BASE_URL}trips/${tripId}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`,
          },
        })

        if (detailsResponse.ok) {
          outboundTrip.value = await detailsResponse.json()
        }
      }
    }

    // Buscar viagem de volta
    const returnResponse = await fetch(
      `${API_BASE_URL}trips/?poll_id=${todayPoll.value.id}&trip_type=return`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      },
    )

    if (returnResponse.ok) {
      const returnTrips = await returnResponse.json()
      if (returnTrips.length > 0) {
        const tripId = returnTrips[0].id
        const detailsResponse = await fetch(`${API_BASE_URL}trips/${tripId}/`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access')}`,
          },
        })

        if (detailsResponse.ok) {
          returnTrip.value = await detailsResponse.json()
        }
      }
    }
  } catch (error) {
    console.error('Error loading trips:', error)
  } finally {
    if (showLoading) {
      isLoading.value = false
    }
  }
}

watch(
  hasActiveTrip,
  (isActive) => {
    if (isActive) {
      startPolling()
    } else {
      stopPolling()
    }
  },
  { immediate: true },
)

onMounted(() => {
  fetchTodayPoll()
})

onUnmounted(() => {
  stopPolling()
})
</script>

<template>
  <DefaultLayout>
    <div class="container mx-auto px-4 py-8 max-w-4xl">
      <div class="mb-8 text-center">
        <h1 class="text-4xl font-bold mb-2">Acompanhamento de Viagem</h1>
        <p class="text-base-content/70">Acompanhe a localização do transporte em tempo real</p>
        <p v-if="lastUpdate" class="text-xs text-base-content/50 mt-2">
          Última atualização: {{ lastUpdate.toLocaleTimeString('pt-BR') }}
        </p>
      </div>

      <TripMessages :error-message="errorMessage" />

      <div v-if="isLoading" class="flex justify-center items-center min-h-[400px]">
        <div class="text-center">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4 text-base-content/70">Carregando viagens...</p>
        </div>
      </div>

      <div v-else-if="!todayPoll" class="alert alert-info">
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
        <span>Não há viagens programadas para hoje</span>
      </div>

      <div v-else class="space-y-6">
        <!-- Viagem de IDA -->
        <div v-if="outboundTrip" class="space-y-6">
          <TripViewCard :trip="outboundTrip" :trip-details="outboundTrip" />

          <CurrentBoardingPoint
            v-if="outboundTrip.status === 'in_progress'"
            :trip-status="outboundTrip.status"
            :trip-details="outboundTrip"
          />

          <AllBoardingPoints :boarding-points="outboundTrip.stops || []" />

          <div v-if="outboundTrip.status === 'pending'" class="alert alert-warning">
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
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <span>A viagem de ida ainda não foi iniciada</span>
          </div>

          <div v-if="outboundTrip.status === 'completed'" class="alert alert-success">
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
            <span>A viagem de ida foi concluída</span>
          </div>
        </div>

        <!-- Viagem de VOLTA -->
        <div v-if="returnTrip" class="space-y-6">
          <TripViewCard :trip="returnTrip" :trip-details="returnTrip" />

          <CurrentBoardingPoint
            v-if="returnTrip.status === 'in_progress'"
            :trip-status="returnTrip.status"
            :trip-details="returnTrip"
          />

          <AllBoardingPoints :boarding-points="returnTrip.stops || []" />

          <div v-if="returnTrip.status === 'pending'" class="alert alert-warning">
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
                d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
              />
            </svg>
            <span>A viagem de volta ainda não foi iniciada</span>
          </div>

          <div v-if="returnTrip.status === 'completed'" class="alert alert-success">
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
            <span>A viagem de volta foi concluída</span>
          </div>
        </div>

        <!-- Sem viagens criadas -->
        <div v-if="!outboundTrip && !returnTrip" class="alert alert-info">
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
          <span>Ainda não há viagens criadas para hoje</span>
        </div>

        <!-- Indicador de atualização automática -->
        <div v-if="hasActiveTrip" class="text-center">
          <div class="badge badge-sm badge-info gap-2">
            <svg
              class="animate-spin h-3 w-3"
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
            Atualizando automaticamente
          </div>
        </div>
      </div>
    </div>
  </DefaultLayout>
</template>
