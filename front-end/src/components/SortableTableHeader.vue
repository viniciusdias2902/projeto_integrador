<script setup>
const props = defineProps({
  label: {
    type: String,
    required: true,
  },
  field: {
    type: String,
    required: true,
  },
  currentSort: {
    type: String,
    default: null,
  },
  currentDirection: {
    type: String,
    default: 'asc',
  },
})

const emit = defineEmits(['sort'])

function handleSort() {
  emit('sort', props.field)
}

const isActive = computed(() => props.currentSort === props.field)
const direction = computed(() => props.currentDirection)
</script>

<template>
  <th class="cursor-pointer select-none hover:bg-base-300" @click="handleSort">
    <div class="flex items-center gap-2">
      <span>{{ label }}</span>
      <div class="flex flex-col">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-3 w-3 transition-opacity"
          :class="isActive && direction === 'asc' ? 'opacity-100' : 'opacity-30'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 15l7-7 7 7" />
        </svg>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-3 w-3 transition-opacity -mt-1"
          :class="isActive && direction === 'desc' ? 'opacity-100' : 'opacity-30'"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M19 9l-7 7-7-7"
          />
        </svg>
      </div>
    </div>
  </th>
</template>
