<script setup>
const props = defineProps({
  boardingPoints: {
    type: Array,
    default: () => [],
  },
})

function getDisplayName(point) {
  if (point.boarding_point) {
    return point.boarding_point.name
  }
  if (point.university_name) {
    return point.university_name
  }
  return 'Ponto desconhecido'
}

function getReference(point) {
  if (point.boarding_point && point.boarding_point.address_reference) {
    return point.boarding_point.address_reference
  }
  return null
}
</script>

<template>
  <div v-if="boardingPoints.length > 0" class="card bg-base-100 shadow-xl">
    <div class="card-body">
      <h3 class="card-title text-xl mb-4">Todos os Pontos</h3>

      <div class="space-y-3">
        <div
          v-for="(point, index) in boardingPoints"
          :key="point.boarding_point?.id || point.university || index"
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
                <h4 class="font-bold">{{ getDisplayName(point) }}</h4>
                <p v-if="getReference(point)" class="text-sm opacity-70">
                  {{ getReference(point) }}
                </p>
              </div>
            </div>
            <div class="badge badge-ghost">{{ point.student_count }} aluno(s)</div>
          </div>

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
            Localização atual
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
