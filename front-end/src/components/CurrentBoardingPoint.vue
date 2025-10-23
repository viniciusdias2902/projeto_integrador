<script setup>
import { computed } from 'vue'

const props = defineProps({
  tripStatus: {
    type: String,
    required: true,
  },
  tripDetails: Object,
})

const currentBoardingPoint = computed(() => {
  if (!props.tripDetails?.boarding_points) return null
  return props.tripDetails.boarding_points.find((bp) => bp.is_current)
})

const currentStudents = computed(() => {
  if (!currentBoardingPoint.value) return []
  return currentBoardingPoint.value.students || []
})
</script>

<template>
  <div
    v-if="tripStatus === 'in_progress' && currentBoardingPoint"
    class="card bg-base-100 shadow-xl"
  >
    <div class="card-body">
      <h3 class="card-title text-xl mb-4">Ponto Atual</h3>

      <div class="bg-primary/10 rounded-box p-4 mb-4">
        <h4 class="font-bold text-lg">{{ currentBoardingPoint.boarding_point.name }}</h4>
        <p v-if="currentBoardingPoint.boarding_point.address_reference" class="text-sm opacity-70">
          {{ currentBoardingPoint.boarding_point.address_reference }}
        </p>
        <div class="badge badge-primary mt-2">
          {{ currentBoardingPoint.student_count }} aluno(s)
        </div>
      </div>

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
</template>
