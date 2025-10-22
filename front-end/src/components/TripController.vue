<script setup>
import { ref, computed, onMounted } from 'vue'

const props = defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

const emit = defineEmits(['trip-updated', 'trip-completed'])

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const tripDetails = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const tripTypeLabel = computed(() => {
  return props.trip.trip_type === 'outbound' ? 'Ida' : 'Volta'
})

const statusLabel = computed(() => {
  const labels = {
    pending: 'Pendente',
    in_progress: 'Em Andamento',
    completed: 'Concluída',
  }
  return labels[props.trip.status] || props.trip.status
})

const statusColor = computed(() => {
  const colors = {
    pending: 'badge-warning',
    in_progress: 'badge-info',
    completed: 'badge-success',
  }
  return colors[props.trip.status] || 'badge-ghost'
})

const currentStudents = computed(() => {
  if (!tripDetails.value?.boarding_points) return []

  const currentPoint = tripDetails.value.boarding_points.find((bp) => bp.is_current)
  return currentPoint?.students || []
})

const currentBoardingPoint = computed(() => {
  if (!tripDetails.value?.boarding_points) return null
  return tripDetails.value.boarding_points.find((bp) => bp.is_current)
})

const progressPercentage = computed(() => {
  if (!tripDetails.value || props.trip.status !== 'in_progress') return 0

  const total = tripDetails.value.total_boarding_points || 0
  const current = tripDetails.value.current_point_index ?? 0

  if (total === 0) return 0
  return Math.round(((current + 1) / total) * 100)
})

// Buscar detalhes completos da viagem
async function fetchTripDetails() {
  isLoading.value = true
  errorMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}trips/${props.trip.id}/`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      throw new Error('Erro ao carregar detalhes da viagem')
    }

    tripDetails.value = await response.json()
  } catch (error) {
    console.error('Error fetching trip details:', error)
    errorMessage.value = 'Erro ao carregar detalhes. Tente novamente.'
  } finally {
    isLoading.value = false
  }
}

async function startTrip() {
  if (props.trip.status !== 'pending') {
    errorMessage.value = 'A viagem já foi iniciada'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}trips/${props.trip.id}/start/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Erro ao iniciar viagem')
    }

    const data = await response.json()
    emit('trip-updated', data.trip)
    successMessage.value = 'Viagem iniciada com sucesso!'

    // Recarregar detalhes
    await fetchTripDetails()
  } catch (error) {
    console.error('Error starting trip:', error)
    errorMessage.value = error.message || 'Erro ao iniciar viagem'
  } finally {
    isLoading.value = false
  }
}

async function nextPoint() {
  if (props.trip.status !== 'in_progress') {
    errorMessage.value = 'A viagem não está em andamento'
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}trips/${props.trip.id}/next_point/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Erro ao avançar para próximo ponto')
    }

    const data = await response.json()

    if (data.completed) {
      successMessage.value = data.message
      emit('trip-completed')
    } else {
      emit('trip-updated', data.trip)
      successMessage.value = 'Avançado para o próximo ponto!'
      await fetchTripDetails()
    }
  } catch (error) {
    console.error('Error moving to next point:', error)
    errorMessage.value = error.message || 'Erro ao avançar para próximo ponto'
  } finally {
    isLoading.value = false
  }
}

// Encerrar viagem manualmente
async function completeTrip() {
  if (props.trip.status !== 'in_progress') {
    errorMessage.value = 'A viagem não está em andamento'
    return
  }

  if (!confirm('Deseja realmente encerrar esta viagem?')) {
    return
  }

  isLoading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await fetch(`${API_BASE_URL}trips/${props.trip.id}/complete/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Bearer ${localStorage.getItem('access')}`,
      },
    })

    if (!response.ok) {
      const error = await response.json()
      throw new Error(error.error || 'Erro ao encerrar viagem')
    }

    const data = await response.json()
    successMessage.value = data.message
    emit('trip-completed')
  } catch (error) {
    console.error('Error completing trip:', error)
    errorMessage.value = error.message || 'Erro ao encerrar viagem'
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  fetchTripDetails()
})
</script>

<template>
  <div class="space-y-6">
    <!-- Cabeçalho da viagem -->
    <div class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <div class="flex items-center justify-between mb-4">
          <div>
            <h2 class="card-title text-2xl">
              {{ tripTypeLabel }}
            </h2>
            <p class="text-base-content/70 text-sm">Viagem #{{ trip.id }}</p>
          </div>
          <div class="badge badge-lg" :class="statusColor">
            {{ statusLabel }}
          </div>
        </div>

        <!-- Barra de progresso -->
        <div v-if="trip.status === 'in_progress' && tripDetails" class="mb-4">
          <div class="flex justify-between text-sm mb-2">
            <span>Progresso</span>
            <span class="font-bold">{{ progressPercentage }}%</span>
          </div>
          <progress
            class="progress progress-primary w-full"
            :value="progressPercentage"
            max="100"
          ></progress>
          <div class="text-xs text-base-content/70 mt-1">
            Ponto {{ (tripDetails.current_point_index ?? 0) + 1 }} de
            {{ tripDetails.total_boarding_points }}
          </div>
        </div>

        <!-- Mensagens -->
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

        <!-- Ações -->
        <div class="card-actions justify-end">
          <button
            v-if="trip.status === 'pending'"
            class="btn btn-primary"
            @click="startTrip"
            :disabled="isLoading"
          >
            <svg
              v-if="!isLoading"
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 mr-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
              />
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
            {{ isLoading ? 'Iniciando...' : 'Iniciar Viagem' }}
          </button>

          <button
            v-if="trip.status === 'in_progress'"
            class="btn btn-primary"
            @click="nextPoint"
            :disabled="isLoading"
          >
            <svg
              v-if="!isLoading"
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5 mr-2"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M13 7l5 5m0 0l-5 5m5-5H6"
              />
            </svg>
            <span v-if="isLoading" class="loading loading-spinner loading-sm"></span>
            {{ isLoading ? 'Avançando...' : 'Próximo Ponto' }}
          </button>

          <button
            v-if="trip.status === 'in_progress'"
            class="btn btn-error btn-outline"
            @click="completeTrip"
            :disabled="isLoading"
          >
            Encerrar Viagem
          </button>

          <button class="btn btn-ghost" @click="fetchTripDetails" :disabled="isLoading">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-5 w-5"
              :class="{ 'animate-spin': isLoading }"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                stroke-linecap="round"
                stroke-linejoin="round"
                stroke-width="2"
                d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"
              />
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Loading detalhes -->
    <div v-if="isLoading && !tripDetails" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <!-- Ponto atual e alunos -->
    <div
      v-if="trip.status === 'in_progress' && currentBoardingPoint"
      class="card bg-base-100 shadow-xl"
    >
      <div class="card-body">
        <h3 class="card-title text-xl mb-4">📍 Ponto Atual</h3>

        <div class="bg-primary/10 rounded-box p-4 mb-4">
          <h4 class="font-bold text-lg">{{ currentBoardingPoint.boarding_point.name }}</h4>
          <p
            v-if="currentBoardingPoint.boarding_point.address_reference"
            class="text-sm opacity-70"
          >
            {{ currentBoardingPoint.boarding_point.address_reference }}
          </p>
          <div class="badge badge-primary mt-2">
            {{ currentBoardingPoint.student_count }} aluno(s)
          </div>
        </div>

        <!-- Lista de alunos -->
        <div v-if="currentStudents.length > 0">
          <h4 class="font-semibold mb-3">Alunos neste ponto:</h4>
          <ul class="menu bg-base-200 rounded-box">
            <li
              v-for="student in currentStudents"
              :key="student.id"
              class="border-b border-base-300 last:border-0"
            >
              <div class="py-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  class="h-5 w-5 opacity-70"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
                <span class="font-medium">{{ student.name }}</span>
              </div>
            </li>
          </ul>
        </div>
        <div v-else class="text-center py-6 opacity-60">Nenhum aluno neste ponto</div>
      </div>
    </div>

    <!-- Todos os pontos (resumo) -->
    <div v-if="tripDetails?.boarding_points" class="card bg-base-100 shadow-xl">
      <div class="card-body">
        <h3 class="card-title text-xl mb-4">Todos os Pontos</h3>

        <div class="space-y-3">
          <div
            v-for="(point, index) in tripDetails.boarding_points"
            :key="point.boarding_point.id"
            class="p-4 rounded-box transition-all"
            :class="{
              'bg-primary/20 border-2 border-primary': point.is_current,
              'bg-base-200': !point.is_current,
            }"
          >
            <div class="flex items-start justify-between">
              <div class="flex items-start gap-3">
                <div class="badge" :class="point.is_current ? 'badge-primary' : 'badge-ghost'">
                  {{ index + 1 }}
                </div>
                <div>
                  <h4 class="font-bold">{{ point.boarding_point.name }}</h4>
                  <p v-if="point.boarding_point.address_reference" class="text-sm opacity-70">
                    {{ point.boarding_point.address_reference }}
                  </p>
                </div>
              </div>
              <div class="badge badge-ghost">{{ point.student_count }} aluno(s)</div>
            </div>

            <!-- Indicador de ponto atual -->
            <div
              v-if="point.is_current"
              class="mt-2 text-sm font-semibold text-primary flex items-center gap-2"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"
                />
              </svg>
              Você está aqui
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
