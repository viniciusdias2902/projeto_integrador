<script setup>
import { computed } from 'vue'

const props = defineProps({
  trip: {
    type: Object,
    required: true,
  },
  tripDetails: Object,
})

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

const progressPercentage = computed(() => {
  if (!props.tripDetails || props.trip.status !== 'in_progress') return 0

  const total = props.tripDetails.total_stops || 0
  const current = props.tripDetails.current_stop_index ?? 0

  if (total === 0) return 0
  return Math.round(((current + 1) / total) * 100)
})
</script>

<template>
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <div class="flex items-center justify-between mb-4">
        <div>
          <h2 class="card-title text-2xl">
            {{ tripTypeLabel }}
          </h2>
          <p class="text-base-content/70 text-sm">Status da viagem</p>
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
          Ponto {{ (tripDetails.current_stop_index ?? 0) + 1 }} de
          {{ tripDetails.total_stops }}
        </div>
      </div>

      <!-- Informações adicionais -->
      <div v-if="trip.started_at" class="text-sm opacity-70">
        <p>
          <strong>Iniciada em:</strong>
          {{ new Date(trip.started_at).toLocaleTimeString('pt-BR') }}
        </p>
      </div>

      <div v-if="trip.completed_at" class="text-sm opacity-70 mt-2">
        <p>
          <strong>Concluída em:</strong>
          {{ new Date(trip.completed_at).toLocaleTimeString('pt-BR') }}
        </p>
      </div>
    </div>
  </div>
</template>
