<script setup>
import { ref, onMounted, computed } from 'vue'
import { verifyAndRefreshToken } from '@/services/auth'
import DefaultLayout from '@/templates/DefaultLayout.vue'
import TripController from '@/components/TripController.vue'

const API_BASE_URL = import.meta.env.VITE_APP_API_URL

const polls = ref([])
const selectedPollId = ref(null)
const outboundTrip = ref(null)
const returnTrip = ref(null)
const isLoading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')

const weekdays = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

const hasActiveTrip = computed(() => outboundTrip.value !== null || returnTrip.value !== null)

const selectedPoll = computed(() => {
  if (!selectedPollId.value) return null
  return polls.value.find((p) => p.id === selectedPollId.value)
})

function formatPollDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const weekday = weekdays[date.getDay()]
  return `${weekday}, ${day}/${month}`
}

async function fetchPolls() {
  errorMessage.value = ''
  isLoading.value = true

  const isValid = verifyAndRefreshToken()
  if (!isValid) {
    errorMessage.value = 'Session expired. Please login again.'
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
      throw new Error('Error loading polls')
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
    errorMessage.value = 'Error loading polls. Please try again.'
  } finally {
    isLoading.value = false
  }
}

async function checkExistingTrips() {
  if (!selectedPollId.value) return

  try {
    const outboundResponse = await fetch(
      `${API_BASE_URL}trips/?poll_id=${selectedPollId.value}&trip_type=outbound`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      },
    )

    if (outboundResponse.ok) {
      const outboundTrips = await outboundResponse.json()
      outboundTrip.value = outboundTrips.length > 0 ? outboundTrips[0] : null
    }

    const returnResponse = await fetch(
      `${API_BASE_URL}trips/?poll_id=${selectedPollId.value}&trip_type=return`,
      {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
      },
    )

    if (returnResponse.ok) {
      const returnTrips = await returnResponse.json()
      returnTrip.value = returnTrips.length > 0 ? returnTrips[0] : null
    }
  } catch (error) {
    console.error('Error checking existing trips:', error)
  }
}

async function initializeTrip() {
  if (!selectedPollId.value) {
    errorMessage.value = 'Please select a poll first'
    return
  }

  errorMessage.value = ''
  successMessage.value = ''
  isLoading.value = true

  try {
    await checkExistingTrips()

    if (!outboundTrip.value) {
      const response = await fetch(`${API_BASE_URL}trips/create/`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${localStorage.getItem('access')}`,
        },
        body: JSON.stringify({
          poll: selectedPollId.value,
          trip_type: 'outbound',
        }),
      })

      if (!response.ok) {
        const error = await response.json()
        throw new Error(error.detail || 'Error creating trip')
      }

      outboundTrip.value = await response.json()
      successMessage.value = 'Trip created successfully'
    } else {
      successMessage.value = 'Trip loaded'
    }
  } catch (error) {
    console.error('Error initializing trip:', error)
    errorMessage.value = error.message || 'Error initializing trip'
  } finally {
    isLoading.value = false
  }
}

function handleOutboundCompleted(returnTripData) {
  outboundTrip.value = null
  if (returnTripData) {
    returnTrip.value = returnTripData
    successMessage.value = 'Outbound trip completed. Return trip ready.'
  }
}

function handleReturnCompleted() {
  returnTrip.value = null
  successMessage.value = 'All trips completed'

  setTimeout(() => {
    successMessage.value = ''
  }, 5000)
}

async function handleSelectionChange() {
  outboundTrip.value = null
  returnTrip.value = null
  if (selectedPollId.value) {
    await checkExistingTrips()
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
        <h1 class="text-4xl font-bold mb-2">Trip Management</h1>
        <p class="text-base-content/70">Control transport trips</p>
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

      <div
        v-if="isLoading && !hasActiveTrip"
        class="flex justify-center items-center min-h-[400px]"
      >
        <div class="text-center">
          <span class="loading loading-spinner loading-lg"></span>
          <p class="mt-4 text-base-content/70">Loading...</p>
        </div>
      </div>

      <div v-else-if="!hasActiveTrip" class="card bg-base-100 shadow-xl">
        <div class="card-body">
          <h2 class="card-title">Select Trip Day</h2>

          <div class="form-control w-full">
            <label class="label">
              <span class="label-text">Poll Day</span>
            </label>
            <select
              v-model="selectedPollId"
              class="select select-bordered w-full"
              @change="handleSelectionChange"
              :disabled="polls.length === 0"
            >
              <option :value="null" disabled>Select a poll</option>
              <option v-for="poll in polls" :key="poll.id" :value="poll.id">
                {{ formatPollDate(poll.date) }}
              </option>
            </select>
          </div>

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
              <p class="text-sm">Round trip (outbound + return)</p>
            </div>
          </div>

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
              {{ isLoading ? 'Loading...' : 'Load Trip' }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="outboundTrip" class="space-y-6">
        <TripController
          :trip="outboundTrip"
          @trip-updated="outboundTrip = $event"
          @trip-completed="handleOutboundCompleted"
        />
      </div>

      <div v-if="returnTrip" class="space-y-6">
        <TripController
          :trip="returnTrip"
          @trip-updated="returnTrip = $event"
          @trip-completed="handleReturnCompleted"
        />
      </div>
    </div>
  </DefaultLayout>
</template>
