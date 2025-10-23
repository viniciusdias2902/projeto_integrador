<script setup>
import { ref, onMounted } from 'vue'
import TripHeader from '@/components/trip/TripHeader.vue'
import TripMessages from '@/components/trip/TripMessages.vue'
import TripActions from '@/components/trip/TripActions.vue'
import CurrentBoardingPoint from '@/components/trip/CurrentBoardingPoint.vue'
import AllBoardingPoints from '@/components/trip/AllBoardingPoints.vue'

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
    <TripHeader :trip="trip" :trip-details="tripDetails" :is-loading="isLoading">
      <TripMessages :error-message="errorMessage" :success-message="successMessage" />

      <TripActions
        :trip-status="trip.status"
        :is-loading="isLoading"
        @start-trip="startTrip"
        @next-point="nextPoint"
        @complete-trip="completeTrip"
        @refresh="fetchTripDetails"
      />
    </TripHeader>

    <div v-if="isLoading && !tripDetails" class="flex justify-center py-12">
      <span class="loading loading-spinner loading-lg"></span>
    </div>

    <CurrentBoardingPoint :trip-status="trip.status" :trip-details="tripDetails" />

    <AllBoardingPoints :boarding-points="tripDetails?.boarding_points || []" />
  </div>
</template>
