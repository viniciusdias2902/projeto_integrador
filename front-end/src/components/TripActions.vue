<script setup>
defineProps({
  tripStatus: {
    type: String,
    required: true,
  },
  isLoading: Boolean,
})

defineEmits(['start-trip', 'next-point', 'complete-trip', 'refresh'])
</script>

<template>
  <div class="card-actions justify-end">
    <button
      v-if="tripStatus === 'pending'"
      class="btn btn-primary"
      @click="$emit('start-trip')"
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
      v-if="tripStatus === 'in_progress'"
      class="btn btn-primary"
      @click="$emit('next-point')"
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
      v-if="tripStatus === 'in_progress'"
      class="btn btn-error btn-outline"
      @click="$emit('complete-trip')"
      :disabled="isLoading"
    >
      Encerrar Viagem
    </button>

    <button class="btn btn-ghost" @click="$emit('refresh')" :disabled="isLoading">
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
</template>
