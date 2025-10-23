<script setup>
const props = defineProps({
  polls: {
    type: Array,
    default: () => [],
  },
  selectedPollId: [Number, null],
  selectedTripType: {
    type: String,
    default: 'outbound',
  },
  selectedPoll: Object,
  isLoading: Boolean,
})

defineEmits(['update:selectedPollId', 'update:selectedTripType', 'initialize-trip'])

const tripTypeOptions = [
  { value: 'outbound', label: 'Ida' },
  { value: 'return', label: 'Volta' },
]

const diasSemana = ['Domingo', 'Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado']

function formatPollDate(dateString) {
  const date = new Date(`${dateString}T00:00:00`)
  const day = String(date.getDate()).padStart(2, '0')
  const month = String(date.getMonth() + 1).padStart(2, '0')
  const weekday = diasSemana[date.getDay()]
  return `${weekday}, ${day}/${month}`
}
</script>

<template>
  <div class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h2 class="card-title">Selecione a Viagem</h2>

      <div class="form-control w-full">
        <label class="label">
          <span class="label-text">Enquete (Dia)</span>
        </label>
        <select
          :value="selectedPollId"
          @change="$emit('update:selectedPollId', Number($event.target.value))"
          class="select select-bordered w-full"
          :disabled="polls.length === 0"
        >
          <option :value="null" disabled>Selecione uma enquete</option>
          <option v-for="poll in polls" :key="poll.id" :value="poll.id">
            {{ formatPollDate(poll.date) }}
          </option>
        </select>
      </div>

      <div class="form-control w-full">
        <label class="label">
          <span class="label-text">Tipo de Viagem</span>
        </label>
        <select
          :value="selectedTripType"
          @change="$emit('update:selectedTripType', $event.target.value)"
          class="select select-bordered w-full"
        >
          <option v-for="option in tripTypeOptions" :key="option.value" :value="option.value">
            {{ option.label }}
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
          <p class="text-sm">{{ selectedTripType === 'outbound' ? 'Ida' : 'Volta' }}</p>
        </div>
      </div>

      <div class="card-actions justify-end mt-4">
        <button
          class="btn btn-primary btn-block"
          @click="$emit('initialize-trip')"
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
</template>
